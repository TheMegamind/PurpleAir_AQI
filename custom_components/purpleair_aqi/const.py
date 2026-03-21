from __future__ import annotations

import logging

from homeassistant.const import Platform

DOMAIN = "purpleair_aqi"
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.NUMBER]
LOGGER = logging.getLogger("custom_components.purpleair_aqi")

# Config entry keys
CONF_DEVICE_SEARCH = "device_search"
CONF_SEARCH_RANGE = "search_range"
CONF_UNIT = "unit"
CONF_WEIGHTED = "weighted"
CONF_SENSOR_INDEX = "sensor_index"
CONF_READ_KEY = "read_key"
CONF_CONVERSION = "conversion"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_NAME = "name"
CONF_PM25_AVERAGING = "pm25_averaging"

# Defaults
DEFAULT_DEVICE_SEARCH = True
DEFAULT_SEARCH_RANGE = 1.5
DEFAULT_UNIT = "miles"
DEFAULT_WEIGHTED = True
DEFAULT_CONVERSION = "US EPA"
DEFAULT_UPDATE_INTERVAL = 10
DEFAULT_PM25_AVERAGING = "10min"

# Conversion options (ordered for UI display)
CONVERSION_OPTIONS = [
    "US EPA",
    "Woodsmoke",
    "AQ&U",
    "LRAPA",
    "CF=1",
    "none",
]

# PM2.5 averaging period options
PM25_AVERAGING_OPTIONS = [
    "real-time",
    "10min",
    "30min",
    "60min",
]

PM25_AVERAGING_FIELD_MAP = {
    "real-time": "pm2.5",
    "10min": "pm2.5_10minute",
    "30min": "pm2.5_30minute",
    "60min": "pm2.5_60minute",
}
