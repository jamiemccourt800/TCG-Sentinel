# TCG-Sentinel

A monitoring and alerting system that tracks Pokémon TCG stock across Irish retailers and hobby shops, plus card shows and events with Pokémon vendors. It detects restocks, new listings, price drops, and event updates, sending real-time alerts via Telegram and Discord.

## Features (Planned)

- **Stock Monitoring**: Track Pokémon TCG products across Irish retailers
- **Event Discovery**: Monitor card shows, comic cons, and gaming events
- **Vendor Tracking**: Alert when known vendors appear at events
- **Multi-Channel Alerts**: Instant notifications via Telegram and Discord
- **Config-Driven**: Add new sources without code changes
- **Smart Filtering**: Keyword and location-based filtering

## Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd TCG-Sentinel
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows CMD:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Validate the setup**
   ```bash
   python scripts/validate_setup.py
   ```

6. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your actual API tokens:
   - Telegram bot token (get from @BotFather)
   - Telegram chat ID (send a message to your bot, then call getUpdates)
   - Discord webhook URLs

## Project Structure

```
TCG-Sentinel/
├── src/                      # Source code
│   ├── collectors/           # Site-specific scrapers/parsers
│   ├── decision_engine/      # Alert generation logic
│   ├── models/               # Data models (Signal, Alert)
│   ├── normalizer/           # Signal normalization and filtering
│   ├── notifiers/            # Telegram and Discord notifiers
│   ├── state_store/          # SQLite database management
│   └── utils/                # Utility functions
├── config/                   # YAML configuration files
├── tests/                    # Test suite
│   └── fixtures/             # Saved HTML for testing parsers
├── scripts/                  # Utility scripts
├── data/                     # SQLite database (gitignored)
└── logs/                     # Application logs (gitignored)
```

## Development Status

**Current Phase**: MVP v1 - Environment Setup ✅

### Roadmap

- [x] Day 1: Environment setup
- [ ] Day 2: Configuration system
- [ ] Day 3-4: First collector and parser (Smyths)
- [ ] Day 5: SQLite database
- [ ] Day 6-7: Decision engine
- [ ] Day 8: Telegram notifier
- [ ] Day 9: Pipeline integration
- [ ] Day 10: Scheduler loop
- [ ] Day 11+: Additional sources and Discord integration

## Usage

*Coming soon - application is under active development*

## License

Private project - all rights reserved
