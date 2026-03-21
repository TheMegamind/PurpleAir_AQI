from __future__ import annotations

from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant

from .api import PurpleAirConfig
from .const import (
    CONF_CONVERSION,
    CONF_DEVICE_SEARCH,
    CONF_PM25_AVERAGING,
    CONF_READ_KEY,
    CONF_SEARCH_RANGE,
    CONF_SENSOR_INDEX,
    CONF_UNIT,
    CONF_UPDATE_INTERVAL,
    CONF_WEIGHTED,
    DEFAULT_CONVERSION,
    DEFAULT_DEVICE_SEARCH,
    DEFAULT_PM25_AVERAGING,
    DEFAULT_SEARCH_RANGE,
    DEFAULT_UNIT,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_WEIGHTED,
    PLATFORMS,
)
from .coordinator import PurpleAirConfigEntry, PurpleAirDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: PurpleAirConfigEntry) -> bool:
    conf = {**entry.data, **entry.options}

    coords = None
    if conf.get(CONF_DEVICE_SEARCH, DEFAULT_DEVICE_SEARCH):
        coords = (float(conf[CONF_LATITUDE]), float(conf[CONF_LONGITUDE]))

    cfg = PurpleAirConfig(
        api_key=conf[CONF_API_KEY],
        device_search=conf.get(CONF_DEVICE_SEARCH, DEFAULT_DEVICE_SEARCH),
        search_coords=coords,
        search_range=float(conf.get(CONF_SEARCH_RANGE, DEFAULT_SEARCH_RANGE)),
        unit=conf.get(CONF_UNIT, DEFAULT_UNIT),
        weighted=conf.get(CONF_WEIGHTED, DEFAULT_WEIGHTED),
        sensor_index=int(conf[CONF_SENSOR_INDEX])
        if conf.get(CONF_SENSOR_INDEX) is not None
        else None,
        read_key=conf.get(CONF_READ_KEY),
        conversion=conf.get(CONF_CONVERSION, DEFAULT_CONVERSION),
        update_interval=int(conf.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)),
        averaging_period=conf.get(CONF_PM25_AVERAGING, DEFAULT_PM25_AVERAGING),
    )

    coordinator = PurpleAirDataUpdateCoordinator(hass, cfg)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PurpleAirConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
