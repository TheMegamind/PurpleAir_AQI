from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .api import PurpleAirResult
from .coordinator import PurpleAirConfigEntry, PurpleAirDataUpdateCoordinator
from .entity import PurpleAirEntity


@dataclass(frozen=True, kw_only=True)
class PurpleAirSensorEntityDescription(SensorEntityDescription):
    """Describes a PurpleAir sensor entity."""

    value_fn: Callable[[PurpleAirResult | None], StateType]


CATEGORY_TO_LEVEL: dict[str, int] = {
    "Good": 1,
    "Moderate": 2,
    "Unhealthy for Sensitive Groups": 3,
    "Unhealthy": 4,
    "Very Unhealthy": 5,
    "Hazardous": 6,
}

CATEGORY_TO_COLOR: dict[str, str] = {
    "Good": "Green",
    "Moderate": "Yellow",
    "Unhealthy for Sensitive Groups": "Orange",
    "Unhealthy": "Red",
    "Very Unhealthy": "Purple",
    "Hazardous": "Maroon",
}

ADVISORY_TEXT: dict[str, str] = {
    "Good": "Air quality is satisfactory. Air pollution poses little or no risk.",
    "Moderate": "Air quality is acceptable. May pose a risk for people unusually sensitive to air pollution.",
    "Unhealthy for Sensitive Groups": "Sensitive groups may experience health effects. The general public is less likely to be affected.",
    "Unhealthy": "Some of the general public may experience health effects. Sensitive groups may experience more serious effects.",
    "Very Unhealthy": "Health alert: the risk of health effects is increased for everyone.",
    "Hazardous": "Health warning of emergency conditions. Everyone is more likely to be affected.",
}

SENSOR_DESCRIPTIONS: tuple[PurpleAirSensorEntityDescription, ...] = (
    PurpleAirSensorEntityDescription(
        key="aqi",
        translation_key="aqi",
        icon="mdi:weather-hazy",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda r: r.aqi if r else None,
    ),
    PurpleAirSensorEntityDescription(
        key="aqi_delta",
        translation_key="aqi_delta",
        icon="mdi:vector-difference",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda r: r.aqi_delta if r else None,
    ),
    PurpleAirSensorEntityDescription(
        key="category",
        translation_key="category",
        device_class=SensorDeviceClass.ENUM,
        options=list(CATEGORY_TO_LEVEL.keys()),
        value_fn=lambda r: r.category if r else None,
    ),
    PurpleAirSensorEntityDescription(
        key="aqi_color",
        translation_key="aqi_color",
        icon="mdi:palette",
        value_fn=lambda r: CATEGORY_TO_COLOR.get(r.category) if r else None,
    ),
    PurpleAirSensorEntityDescription(
        key="conversion",
        translation_key="conversion",
        icon="mdi:flask-outline",
        value_fn=lambda r: r.conversion if r else None,
    ),
    PurpleAirSensorEntityDescription(
        key="health_advisory",
        translation_key="health_advisory",
        icon="mdi:head-question-outline",
        value_fn=lambda r: ADVISORY_TEXT.get(r.category) if r else None,
    ),
    PurpleAirSensorEntityDescription(
        key="health_status",
        translation_key="health_status",
        value_fn=lambda r: "online" if r else "offline",
    ),
    PurpleAirSensorEntityDescription(
        key="sites",
        translation_key="sites",
        icon="mdi:map-marker-multiple-outline",
        value_fn=lambda r: ", ".join(r.sites) if r and r.sites else None,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PurpleAirConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    async_add_entities(
        PurpleAirSensorEntity(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class PurpleAirSensorEntity(PurpleAirEntity, SensorEntity):
    """A sensor entity driven by a PurpleAirSensorEntityDescription."""

    entity_description: PurpleAirSensorEntityDescription

    def __init__(
        self,
        coordinator: PurpleAirDataUpdateCoordinator,
        entry: PurpleAirConfigEntry,
        description: PurpleAirSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> StateType:
        return self.entity_description.value_fn(self.coordinator.data)
