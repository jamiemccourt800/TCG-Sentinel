#!/usr/bin/env python
"""
Quick validation script to test the environment setup.
Run this to verify all dependencies are installed correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    
    try:
        import requests
        print("✓ requests")
        
        import bs4
        print("✓ beautifulsoup4")
        
        import yaml
        print("✓ pyyaml")
        
        from dotenv import load_dotenv
        print("✓ python-dotenv")
        
        import telegram
        print("✓ python-telegram-bot")
        
        import dateutil
        print("✓ python-dateutil")
        
        import pytest
        print("✓ pytest")
        
        import sqlite3
        print("✓ sqlite3 (built-in)")
        
        print("\nAll dependencies installed successfully!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        return False

def check_directory_structure():
    """Verify the project directory structure is correct."""
    print("\nChecking directory structure...")
    
    base_dir = Path(__file__).parent.parent
    required_dirs = [
        "src",
        "src/models",
        "src/collectors",
        "src/collectors/parsers",
        "src/normalizer",
        "src/state_store",
        "src/state_store/migrations",
        "src/decision_engine",
        "src/notifiers",
        "src/notifiers/templates",
        "src/utils",
        "config",
        "tests",
        "tests/fixtures",
        "scripts",
        "data",
        "logs",
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ (missing)")
            all_exist = False
    
    if all_exist:
        print("\nAll directories are present")
    else:
        print("\nSome directories are missing")
    
    return all_exist

def check_files():
    """Check that essential files exist."""
    print("\nChecking essential files...")
    
    base_dir = Path(__file__).parent.parent
    required_files = [
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (missing)")
            all_exist = False
    
    if all_exist:
        print("\nAll essential files present")
    else:
        print("\nSome files are missing")
    
    return all_exist

def main():
    """Run all validation checks."""
    print("=" * 60)
    print("TCG-Sentinel Environment Validation")
    print("=" * 60)
    print()
    
    results = [
        test_imports(),
        check_directory_structure(),
        check_files(),
    ]
    
    print("\n" + "=" * 60)
    if all(results):
        print("\nEnvironment setup complete\n")
        return 0
    else:
        print("Some checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
