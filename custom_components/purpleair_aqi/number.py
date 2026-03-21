from __future__ import annotations

from datetime import timedelta

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
from .coordinator import PurpleAirConfigEntry, PurpleAirDataUpdateCoordinator
from .entity import PurpleAirEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PurpleAirConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    async_add_entities([PurpleAirUpdateIntervalNumber(coordinator, entry)])


class PurpleAirUpdateIntervalNumber(PurpleAirEntity, NumberEntity):
    """Polling interval control."""

    _attr_translation_key = "update_interval"
    _attr_icon = "mdi:timer-outline"
    _attr_native_min_value = 1
    _attr_native_max_value = 60
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_mode = NumberMode.SLIDER

    def __init__(
        self, coordinator: PurpleAirDataUpdateCoordinator, entry: PurpleAirConfigEntry
    ) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_update_interval"

    @property
    def native_value(self) -> int:
        merged = {**self.entry.data, **self.entry.options}
        return int(merged.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL))

    async def async_set_native_value(self, value: float) -> None:
        minutes = int(value)

        new_options = {**self.entry.options, CONF_UPDATE_INTERVAL: minutes}
        self.hass.config_entries.async_update_entry(self.entry, options=new_options)

        self.coordinator.update_interval = timedelta(minutes=minutes)
        await self.coordinator.async_request_refresh()
