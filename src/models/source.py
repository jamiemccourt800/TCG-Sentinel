"""
Source configuration model.
Represents a monitoring target (website, API, etc).
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Source:
    """Configuration for a single monitoring source."""
    
    name: str                           # Unique identifier (e.g., "smyths_pokemon")
    type: str                           # "retail_category" | "event_list" | "event_vendor"
    url: str                            # Target URL to monitor
    parser_key: str                     # Which parser to use (e.g., "smyths_category")
    poll_interval: int                  # Seconds between polls
    tags: List[str] = field(default_factory=list)  # ["retailer", "ireland", etc]
    enabled: bool = True                # Whether to actively monitor
    description: Optional[str] = None   # Human-readable description
    
    def __post_init__(self):
        """Validate the source configuration."""
        if not self.name:
            raise ValueError("Source name is required")
        
        if not self.url:
            raise ValueError(f"URL is required for source: {self.name}")
        
        if self.type not in ["retail_category", "event_list", "event_vendor"]:
            raise ValueError(f"Invalid source type '{self.type}' for {self.name}")
        
        if self.poll_interval < 60:
            raise ValueError(f"Poll interval too short for {self.name} (min 60 seconds)")
    
    def should_poll(self, last_poll_time: float, current_time: float) -> bool:
        """
        Check if this source is due for polling.
        
        Args:
            last_poll_time: Unix timestamp of last poll
            current_time: Current unix timestamp
            
        Returns:
            True if enough time has elapsed since last poll
        """
        if not self.enabled:
            return False
        
        if last_poll_time is None:
            return True
        
        elapsed = current_time - last_poll_time
        return elapsed >= self.poll_interval
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Source(name={self.name}, type={self.type}, enabled={self.enabled})"
