"""
Configuration loader for TCG Sentinel.
Loads and validates YAML configuration files.
"""

import os
from pathlib import Path
from typing import Dict, List, Any

import yaml
from dotenv import load_dotenv

from src.models.source import Source


class Config:
    """Main configuration container for the application."""
    
    def __init__(self, config_dir: Path = None):
        """
        Initialize configuration from YAML files.
        
        Args:
            config_dir: Path to config directory (defaults to ./config)
        """
        if config_dir is None:
            # Default to config/ directory in project root
            project_root = Path(__file__).parent.parent
            config_dir = project_root / "config"
        
        self.config_dir = Path(config_dir)
        
        # Load environment variables
        load_dotenv()
        
        # Load all configuration files
        self.sources: List[Source] = self._load_sources()
        self.keywords: Dict[str, List[str]] = self._load_keywords()
        self.routing: Dict[str, Any] = self._load_routing()
        self.thresholds: Dict[str, Any] = self._load_thresholds()
        
        # Environment-based settings
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.discord_webhook_stock = os.getenv("DISCORD_WEBHOOK_STOCK")
        self.discord_webhook_events = os.getenv("DISCORD_WEBHOOK_EVENTS")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.database_path = os.getenv("DATABASE_PATH", "data/tcg_sentinel.db")
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load a YAML file from the config directory.
        
        Args:
            filename: Name of the YAML file (e.g., "sources.yaml")
            
        Returns:
            Parsed YAML data as dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        file_path = self.config_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _load_sources(self) -> List[Source]:
        """
        Load source configurations from sources.yaml.
        
        Returns:
            List of Source objects
        """
        data = self._load_yaml("sources.yaml")
        sources = []
        
        for source_data in data.get("sources", []):
            try:
                source = Source(
                    name=source_data["name"],
                    type=source_data["type"],
                    url=source_data["url"],
                    parser_key=source_data["parser_key"],
                    poll_interval=source_data["poll_interval"],
                    tags=source_data.get("tags", []),
                    enabled=source_data.get("enabled", True),
                    description=source_data.get("description"),
                )
                sources.append(source)
            except (KeyError, ValueError) as e:
                print(f"Warning: Skipping invalid source: {e}")
                continue
        
        return sources
    
    def _load_keywords(self) -> Dict[str, List[str]]:
        """
        Load keyword filters from keywords.yaml.
        
        Returns:
            Dictionary with 'allowlist' and 'blocklist' keys
        """
        data = self._load_yaml("keywords.yaml")
        
        return {
            "allowlist": [kw.lower() for kw in data.get("allowlist", [])],
            "blocklist": [kw.lower() for kw in data.get("blocklist", [])],
        }
    
    def _load_routing(self) -> Dict[str, Any]:
        """
        Load alert routing configuration from routing.yaml.
        
        Returns:
            Dictionary mapping alert types to channel configs
        """
        return self._load_yaml("routing.yaml").get("routing", {})
    
    def _load_thresholds(self) -> Dict[str, Any]:
        """
        Load thresholds and cooldowns from thresholds.yaml.
        
        Returns:
            Dictionary with cooldowns, thresholds, and filters
        """
        return self._load_yaml("thresholds.yaml")
    
    def get_enabled_sources(self) -> List[Source]:
        """Get only enabled sources."""
        return [s for s in self.sources if s.enabled]
    
    def get_source_by_name(self, name: str) -> Source:
        """
        Get a specific source by name.
        
        Args:
            name: Source name to look up
            
        Returns:
            Source object
            
        Raises:
            KeyError: If source not found
        """
        for source in self.sources:
            if source.name == name:
                return source
        raise KeyError(f"Source not found: {name}")
    
    def get_sources_by_type(self, source_type: str) -> List[Source]:
        """Get all sources of a specific type."""
        return [s for s in self.sources if s.type == source_type]
    
    def has_keyword_match(self, text: str) -> bool:
        """
        Check if text contains allowlist keywords and no blocklist keywords.
        
        Args:
            text: Text to check (e.g., product title)
            
        Returns:
            True if text matches filter criteria
        """
        text_lower = text.lower()
        
        # Check blocklist first (faster rejection)
        for blocked_word in self.keywords["blocklist"]:
            if blocked_word in text_lower:
                return False
        
        # Check allowlist
        for allowed_word in self.keywords["allowlist"]:
            if allowed_word in text_lower:
                return True
        
        return False
    
    def get_cooldown(self, alert_type: str) -> int:
        """
        Get cooldown period for an alert type.
        
        Args:
            alert_type: Type of alert (e.g., "stock_in")
            
        Returns:
            Cooldown in seconds (0 = no cooldown)
        """
        return self.thresholds.get("cooldowns", {}).get(alert_type, 0)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Config(sources={len(self.sources)}, "
                f"enabled={len(self.get_enabled_sources())})")


def load_config(config_dir: Path = None) -> Config:
    """
    Convenience function to load configuration.
    
    Args:
        config_dir: Optional path to config directory
        
    Returns:
        Configured Config object
    """
    return Config(config_dir=config_dir)
