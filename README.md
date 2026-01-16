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
   git clone <repo-url>
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
   Then edit `.env` with API tokens:
   - Telegram bot token 
   - Telegram chat ID 
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

**Current Phase**: MVP v1 - Environment Setup

## Usage

*Coming soon - application is under active development*

## License

Private project - all rights reserved
