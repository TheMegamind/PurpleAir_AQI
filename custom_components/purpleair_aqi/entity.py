from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_NAME, DOMAIN
from .coordinator import PurpleAirConfigEntry, PurpleAirDataUpdateCoordinator


class PurpleAirEntity(CoordinatorEntity[PurpleAirDataUpdateCoordinator]):
    """Base entity for all PurpleAir entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PurpleAirDataUpdateCoordinator,
        entry: PurpleAirConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self.entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data.get(CONF_NAME, "PurpleAir AQI"),
            manufacturer="PurpleAir",
        )
