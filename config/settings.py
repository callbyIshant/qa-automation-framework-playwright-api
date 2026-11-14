"""
Centralized configuration — reads from .env, never hardcodes secrets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


# ── UI Settings ──
BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
VALID_USER: str = os.getenv("VALID_USER", "standard_user")
LOCKED_USER: str = os.getenv("LOCKED_USER", "locked_out_user")
PASSWORD: str = os.getenv("PASSWORD", "secret_sauce")

# ── API Settings ──
API_BASE_URL: str = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")
API_USERNAME: str = os.getenv("API_USERNAME", "admin")
API_PASSWORD: str = os.getenv("API_PASSWORD", "password123")

# ── Playwright Settings ──
HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
BROWSER: str = os.getenv("BROWSER", "chromium")
