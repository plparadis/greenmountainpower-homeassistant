"""Constants for Green Mountain Power Home Assistant."""

from datetime import timedelta

# Base component constants
NAME = "Green Mountain Power"
DOMAIN = "greenmountainpower"
VERSION = "0.1.0"

ISSUE_URL = "https://github.com/plparadis/greenmountainpower-homeassistant/issues"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_ACCOUNT_NUMBER = "account_number"
CONF_PRICE_PER_KWH = "price_per_kwh"
CONF_BACKFILL_DAYS = "backfill_days"

# Defaults
DEFAULT_BACKFILL_DAYS = 365
DEFAULT_PRICE_PER_KWH = 0.0

SCAN_INTERVAL = timedelta(minutes=30)
