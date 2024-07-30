"""Sensor number for stiebel_eltron_isg."""
import logging

from homeassistant.const import (
    UnitOfTemperature,
)

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)
from .const import (
    DOMAIN,
    COMFORT_TEMPERATURE_TARGET_HK1,
    ECO_TEMPERATURE_TARGET_HK1,
    HEATING_CURVE_RISE_HK1,
    COMFORT_TEMPERATURE_TARGET_HK2,
    ECO_TEMPERATURE_TARGET_HK2,
    HEATING_CURVE_RISE_HK2,
    COMFORT_TEMPERATURE_TARGET_HK3,
    ECO_TEMPERATURE_TARGET_HK3,
    HEATING_CURVE_RISE_HK3,
    COMFORT_WATER_TEMPERATURE_TARGET,
    ECO_WATER_TEMPERATURE_TARGET,
    AREA_COOLING_TARGET_ROOM_TEMPERATURE,
    AREA_COOLING_TARGET_FLOW_TEMPERATURE,
    FAN_COOLING_TARGET_ROOM_TEMPERATURE,
    FAN_COOLING_TARGET_FLOW_TEMPERATURE,
    FAN_LEVEL_DAY,
    FAN_LEVEL_NIGHT
)
from .entity import StiebelEltronISGEntity

_LOGGER = logging.getLogger(__name__)


NUMBER_TYPES_ALL = [
    NumberEntityDescription(
        COMFORT_TEMPERATURE_TARGET_HK1,
        has_entity_name=True,
        name="Comfort Temperature Target HK1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=5,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        ECO_TEMPERATURE_TARGET_HK1,
        has_entity_name=True,
        name="Eco Temperature Target HK1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=5,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        COMFORT_TEMPERATURE_TARGET_HK2,
        has_entity_name=True,
        name="Comfort Temperature Target HK2",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=5,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        ECO_TEMPERATURE_TARGET_HK2,
        has_entity_name=True,
        name="Eco Temperature Target HK2",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=5,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        COMFORT_TEMPERATURE_TARGET_HK3,
        has_entity_name=True,
        name="Comfort Temperature Target HK3",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=5,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        ECO_TEMPERATURE_TARGET_HK3,
        has_entity_name=True,
        name="Eco Temperature Target HK3",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=5,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        COMFORT_WATER_TEMPERATURE_TARGET,
        has_entity_name=True,
        name="Comfort Water Temperature Target",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=10,
        native_max_value=75,
        native_step=0.1,
    ),
    NumberEntityDescription(
        ECO_WATER_TEMPERATURE_TARGET,
        has_entity_name=True,
        name="Eco Water Temperature Target",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=10,
        native_max_value=75,
        native_step=0.1,
    ),
    NumberEntityDescription(
        AREA_COOLING_TARGET_ROOM_TEMPERATURE,
        has_entity_name=True,
        name="Area Cooling Room Temperature Target",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=20,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        AREA_COOLING_TARGET_FLOW_TEMPERATURE,
        has_entity_name=True,
        name="Area Cooling Flow Temperature Target",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=7,
        native_max_value=25,
        native_step=0.1,
    ),
    NumberEntityDescription(
        FAN_COOLING_TARGET_ROOM_TEMPERATURE,
        has_entity_name=True,
        name="Fan Cooling Room Temperature Target",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=20,
        native_max_value=30,
        native_step=0.1,
    ),
    NumberEntityDescription(
        FAN_COOLING_TARGET_FLOW_TEMPERATURE,
        has_entity_name=True,
        name="Fan Cooling Flow Temperature Target",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="hass:thermometer",
        native_min_value=7,
        native_max_value=25,
        native_step=0.1,
    ),
]

NUMBER_TYPES_WPM = [
    NumberEntityDescription(
        HEATING_CURVE_RISE_HK1,
        has_entity_name=True,
        name="Heating Curve Rise HK1",
        icon="hass:thermometer",
        native_min_value=0,
        native_max_value=3,
        native_step=0.01,
    ),
    NumberEntityDescription(
        HEATING_CURVE_RISE_HK2,
        has_entity_name=True,
        name="Heating Curve Rise HK2",
        icon="hass:thermometer",
        native_min_value=0,
        native_max_value=3,
        native_step=0.01,
    ),
     NumberEntityDescription(
        HEATING_CURVE_RISE_HK3,
        has_entity_name=True,
        name="Heating Curve Rise HK3",
        icon="hass:thermometer",
        native_min_value=0,
        native_max_value=3,
        native_step=0.01,
    ),
]


NUMBER_TYPES_LWZ = [
    NumberEntityDescription(
        FAN_LEVEL_DAY,
        has_entity_name=True,
        name="Fan Level Day",
        icon="mdi:fan",
        native_min_value=0,
        native_max_value=3,
        native_step=1,
    ),
    NumberEntityDescription(
        FAN_LEVEL_NIGHT,
        has_entity_name=True,
        name="Fan Level Night",
        icon="mdi:fan",
        native_min_value=0,
        native_max_value=3,
        native_step=1,
    ),
    # Add HEATING_CURVE_RISE with max value 5
]


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for description in NUMBER_TYPES_ALL:
        select_entity = StiebelEltronISGNumberEntity(coordinator, entry, description)
        entities.append(select_entity)
    if coordinator.is_wpm:
        for description in NUMBER_TYPES_WPM:
            select_entity = StiebelEltronISGNumberEntity(
                coordinator, entry, description
            )
            entities.append(select_entity)
    # else:
    for description in NUMBER_TYPES_LWZ:
        select_entity = StiebelEltronISGNumberEntity(coordinator, entry, description)
        entities.append(select_entity)
    async_add_devices(entities)


class StiebelEltronISGNumberEntity(StiebelEltronISGEntity, NumberEntity):
    """stiebel_eltron_isg select class."""

    def __init__(self, coordinator, config_entry, description):
        """Initialize the sensor."""
        self.entity_description = description
        super().__init__(coordinator, config_entry)

    @property
    def unique_id(self) -> str | None:
        """Return the unique id of the select entity."""
        return f"{DOMAIN}_{self.coordinator.name}_{self.entity_description.key}"

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        self.coordinator.set_data(self.entity_description.key, value)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data.get(self.entity_description.key) is not None
