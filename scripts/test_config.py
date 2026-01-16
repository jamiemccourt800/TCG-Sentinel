#!/usr/bin/env python
"""
Test script to verify configuration loading.
Run this to ensure all YAML configs are valid and can be loaded.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_loader import load_config


def main():
    """Load and display configuration."""
    print("=" * 60)
    print("TCG-Sentinel Configuration Test")
    print("=" * 60)
    print()
    
    try:
        # Load configuration
        print("Loading configuration...")
        config = load_config()
        print("✓ Configuration loaded successfully\n")
        
        # Display sources
        print(f"Sources ({len(config.sources)} total, {len(config.get_enabled_sources())} enabled):")
        print("-" * 60)
        for source in config.sources:
            status = "✓" if source.enabled else "✗"
            interval_min = source.poll_interval / 60
            print(f"{status} {source.name}")
            print(f"  Type: {source.type}")
            print(f"  URL: {source.url}")
            print(f"  Parser: {source.parser_key}")
            print(f"  Interval: {interval_min:.1f} minutes")
            print(f"  Tags: {', '.join(source.tags)}")
            if source.description:
                print(f"  Description: {source.description}")
            print()
        
        # Display keywords
        print(f"\nKeywords:")
        print("-" * 60)
        print(f"Allowlist: {len(config.keywords['allowlist'])} keywords")
        print(f"  Examples: {', '.join(config.keywords['allowlist'][:5])}")
        print(f"Blocklist: {len(config.keywords['blocklist'])} keywords")
        print(f"  Examples: {', '.join(config.keywords['blocklist'][:5])}")
        print()
        
        # Test keyword matching
        print("\nKeyword Matching Tests:")
        print("-" * 60)
        test_cases = [
            ("Pokemon TCG Booster Box", True),
            ("Elite Trainer Box Scarlet Violet", True),
            ("Yu-Gi-Oh Booster Pack", False),
            ("Magic The Gathering Cards", False),
            ("Obsidian Flames ETB", True),
        ]
        
        for text, expected in test_cases:
            result = config.has_keyword_match(text)
            status = "✓" if result == expected else "✗"
            match_str = "MATCH" if result else "NO MATCH"
            print(f"{status} '{text}' -> {match_str}")
        print()
        
        # Display routing
        print("\nAlert Routing:")
        print("-" * 60)
        for alert_type, routing in config.routing.items():
            telegram = "✓" if routing.get("telegram") else "✗"
            discord = routing.get("discord", "none")
            priority = routing.get("priority", "normal")
            print(f"{alert_type:20s} -> Telegram:{telegram} Discord:{discord} Priority:{priority}")
        print()
        
        # Display thresholds
        print("\nThresholds:")
        print("-" * 60)
        cooldowns = config.thresholds.get("cooldowns", {})
        for alert_type, seconds in cooldowns.items():
            if seconds == 0:
                cooldown_str = "No cooldown"
            elif seconds < 3600:
                cooldown_str = f"{seconds / 60:.0f} minutes"
            elif seconds < 86400:
                cooldown_str = f"{seconds / 3600:.1f} hours"
            else:
                cooldown_str = f"{seconds / 86400:.1f} days"
            print(f"{alert_type:20s}: {cooldown_str}")
        
        price_threshold = config.thresholds.get("price_drop_threshold", 0)
        print(f"\nPrice drop threshold: {price_threshold * 100:.0f}%")
        
        max_alerts = config.thresholds.get("max_alerts_per_hour", 0)
        print(f"Max alerts per hour: {max_alerts}")
        
        # Geo filter
        geo_filter = config.thresholds.get("geo_filter", {})
        if geo_filter.get("enabled"):
            counties = geo_filter.get("allowed_counties", [])
            print(f"\nGeo filtering: Enabled")
            print(f"Allowed counties: {', '.join(counties)}")
        print()
        
        # Environment variables (without showing secrets)
        print("\nEnvironment Variables:")
        print("-" * 60)
        telegram_status = "✓ Set" if config.telegram_token else "✗ Not set"
        discord_stock_status = "✓ Set" if config.discord_webhook_stock else "✗ Not set"
        discord_events_status = "✓ Set" if config.discord_webhook_events else "✗ Not set"
        
        print(f"TELEGRAM_BOT_TOKEN: {telegram_status}")
        print(f"TELEGRAM_CHAT_ID: {'✓ Set' if config.telegram_chat_id else '✗ Not set'}")
        print(f"DISCORD_WEBHOOK_STOCK: {discord_stock_status}")
        print(f"DISCORD_WEBHOOK_EVENTS: {discord_events_status}")
        print(f"LOG_LEVEL: {config.log_level}")
        print(f"DATABASE_PATH: {config.database_path}")
        print()
        
        print("Configuration is valid and ready to use")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Configuration error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
