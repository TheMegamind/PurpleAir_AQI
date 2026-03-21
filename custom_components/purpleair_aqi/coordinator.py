from __future__ import annotations

from datetime import timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PurpleAirClient, PurpleAirConfig, PurpleAirResult
from .const import DOMAIN, LOGGER

# Type alias used wherever a config entry is referenced — mirrors official HA pattern.
# Uses Python 3.12 'type' statement for lazy evaluation (forward reference safe).
type PurpleAirConfigEntry = ConfigEntry[PurpleAirDataUpdateCoordinator]


class PurpleAirDataUpdateCoordinator(DataUpdateCoordinator[PurpleAirResult]):
    """Manages polling the PurpleAir API and tracking AQI delta between updates."""

    config_entry: PurpleAirConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        cfg: PurpleAirConfig,
    ) -> None:
        self._client = PurpleAirClient(async_get_clientsession(hass), cfg)
        self._last_aqi: int | None = None
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=cfg.update_interval),
        )

    async def _async_update_data(self) -> PurpleAirResult:
        try:
            data = await self._client.fetch()
        except aiohttp.ClientError as err:
            raise UpdateFailed(
                f"Network error communicating with PurpleAir: {err}"
            ) from err
        except RuntimeError as err:
            raise UpdateFailed(str(err)) from err

        data.aqi_delta = 0 if self._last_aqi is None else data.aqi - self._last_aqi
        self._last_aqi = data.aqi

        return data
