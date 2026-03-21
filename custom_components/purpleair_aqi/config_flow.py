from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback

from .const import (
    CONF_CONVERSION,
    CONF_DEVICE_SEARCH,
    CONF_NAME,
    CONF_PM25_AVERAGING,
    CONF_READ_KEY,
    CONF_SEARCH_RANGE,
    CONF_SENSOR_INDEX,
    CONF_UNIT,
    CONF_UPDATE_INTERVAL,
    CONF_WEIGHTED,
    CONVERSION_OPTIONS,
    DEFAULT_CONVERSION,
    DEFAULT_DEVICE_SEARCH,
    DEFAULT_PM25_AVERAGING,
    DEFAULT_SEARCH_RANGE,
    DEFAULT_UNIT,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_WEIGHTED,
    DOMAIN,
    PM25_AVERAGING_OPTIONS,
)
from .coordinator import PurpleAirConfigEntry


class PurpleAirConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PurpleAir — two steps: credentials/mode, then location or sensor."""

    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: PurpleAirConfigEntry,
    ) -> PurpleAirOptionsFlow:
        return PurpleAirOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Step 1: collect API key and search mode."""
        if user_input is not None:
            self._data.update(user_input)
            if user_input.get(CONF_DEVICE_SEARCH, DEFAULT_DEVICE_SEARCH):
                return await self.async_step_by_coordinates()
            return await self.async_step_by_sensor()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_NAME, default="PurpleAir AQI"): str,
                    vol.Required(
                        CONF_DEVICE_SEARCH, default=DEFAULT_DEVICE_SEARCH
                    ): bool,
                }
            ),
        )

    async def async_step_by_coordinates(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Step 2a: location-based area search settings."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(
                title=self._data.get(CONF_NAME, "PurpleAir AQI"), data=self._data
            )

        default_lat = self.hass.config.latitude
        default_lon = self.hass.config.longitude

        return self.async_show_form(
            step_id="by_coordinates",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_LATITUDE, default=default_lat): vol.Coerce(float),
                    vol.Optional(CONF_LONGITUDE, default=default_lon): vol.Coerce(
                        float
                    ),
                    vol.Optional(
                        CONF_SEARCH_RANGE, default=DEFAULT_SEARCH_RANGE
                    ): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=50)),
                    vol.Optional(CONF_UNIT, default=DEFAULT_UNIT): vol.In(
                        ["miles", "kilometers"]
                    ),
                    vol.Optional(CONF_WEIGHTED, default=DEFAULT_WEIGHTED): bool,
                    vol.Optional(CONF_CONVERSION, default=DEFAULT_CONVERSION): vol.In(
                        CONVERSION_OPTIONS
                    ),
                    vol.Optional(
                        CONF_PM25_AVERAGING, default=DEFAULT_PM25_AVERAGING
                    ): vol.In(PM25_AVERAGING_OPTIONS),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
                    ): vol.Coerce(int),
                }
            ),
        )

    async def async_step_by_sensor(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Step 2b: direct private sensor settings."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(
                title=self._data.get(CONF_NAME, "PurpleAir AQI"), data=self._data
            )

        return self.async_show_form(
            step_id="by_sensor",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SENSOR_INDEX): vol.Coerce(int),
                    vol.Optional(CONF_READ_KEY): str,
                    vol.Optional(CONF_CONVERSION, default=DEFAULT_CONVERSION): vol.In(
                        CONVERSION_OPTIONS
                    ),
                    vol.Optional(
                        CONF_PM25_AVERAGING, default=DEFAULT_PM25_AVERAGING
                    ): vol.In(PM25_AVERAGING_OPTIONS),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
                    ): vol.Coerce(int),
                }
            ),
        )


class PurpleAirOptionsFlow(config_entries.OptionsFlowWithReload):
    """Options flow — edits mutable settings; triggers automatic entry reload on save."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        # Merge entry.data and entry.options so existing values always appear as defaults,
        # regardless of whether they were stored before the data/options split was introduced.
        current = {**self.config_entry.data, **self.config_entry.options}
        device_search: bool = self.config_entry.data.get(
            CONF_DEVICE_SEARCH, DEFAULT_DEVICE_SEARCH
        )

        if user_input is not None:
            # Extract fields that must live in entry.data (not entry.options).
            data_updates: dict[str, Any] = {CONF_NAME: user_input.pop(CONF_NAME)}
            if device_search:
                data_updates[CONF_LATITUDE] = user_input.pop(CONF_LATITUDE)
                data_updates[CONF_LONGITUDE] = user_input.pop(CONF_LONGITUDE)

            self.hass.config_entries.async_update_entry(
                self.config_entry,
                title=data_updates[CONF_NAME],
                data={**self.config_entry.data, **data_updates},
            )

            # Remaining keys go to entry.options.
            return self.async_create_entry(title="", data=user_input)

        if device_search:
            schema = vol.Schema(
                {
                    vol.Optional(
                        CONF_LATITUDE,
                        default=self.config_entry.data.get(
                            CONF_LATITUDE, self.hass.config.latitude
                        ),
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_LONGITUDE,
                        default=self.config_entry.data.get(
                            CONF_LONGITUDE, self.hass.config.longitude
                        ),
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_SEARCH_RANGE,
                        default=current.get(CONF_SEARCH_RANGE, DEFAULT_SEARCH_RANGE),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=50)),
                    vol.Optional(
                        CONF_UNIT,
                        default=current.get(CONF_UNIT, DEFAULT_UNIT),
                    ): vol.In(["miles", "kilometers"]),
                    vol.Optional(
                        CONF_WEIGHTED,
                        default=current.get(CONF_WEIGHTED, DEFAULT_WEIGHTED),
                    ): bool,
                    vol.Optional(
                        CONF_CONVERSION,
                        default=current.get(CONF_CONVERSION, DEFAULT_CONVERSION),
                    ): vol.In(CONVERSION_OPTIONS),
                    vol.Optional(
                        CONF_PM25_AVERAGING,
                        default=current.get(
                            CONF_PM25_AVERAGING, DEFAULT_PM25_AVERAGING
                        ),
                    ): vol.In(PM25_AVERAGING_OPTIONS),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=current.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                    ): vol.Coerce(int),
                    vol.Optional(
                        CONF_NAME,
                        default=self.config_entry.data.get(CONF_NAME, "PurpleAir AQI"),
                    ): str,
                }
            )
        else:
            schema = vol.Schema(
                {
                    vol.Optional(
                        CONF_CONVERSION,
                        default=current.get(CONF_CONVERSION, DEFAULT_CONVERSION),
                    ): vol.In(CONVERSION_OPTIONS),
                    vol.Optional(
                        CONF_PM25_AVERAGING,
                        default=current.get(
                            CONF_PM25_AVERAGING, DEFAULT_PM25_AVERAGING
                        ),
                    ): vol.In(PM25_AVERAGING_OPTIONS),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=current.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                    ): vol.Coerce(int),
                    vol.Optional(
                        CONF_NAME,
                        default=self.config_entry.data.get(CONF_NAME, "PurpleAir AQI"),
                    ): str,
                }
            )

        return self.async_show_form(step_id="init", data_schema=schema)
