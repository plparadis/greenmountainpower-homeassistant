"""Constants for the GMP HA integration."""
from __future__ import annotations

from datetime import timedelta

# Base component constants
NAME = "GMP HA"
DOMAIN = "gmp_ha"
VERSION = "0.1.0"

ISSUE_URL = "https://github.com/plparadis/gmp-ha/issues"

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
DEFAULT_BACKFILL_DAYS = 30
DEFAULT_PRICE_PER_KWH = 0.0

SCAN_INTERVAL = timedelta(minutes=30)
