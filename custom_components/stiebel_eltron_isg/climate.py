"""Climate platform for stiebel_eltron_isg."""
import logging


from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityDescription,
    HVACMode,
    ClimateEntityFeature,
    FAN_OFF,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    PRESET_ECO,
    PRESET_COMFORT,
)
from homeassistant.const import UnitOfTemperature


from .const import (
    DOMAIN,
    ACTUAL_HUMIDITY,
    ACTUAL_TEMPERATURE,
    ACTUAL_TEMPERATURE_FEK,
    COMFORT_TEMPERATURE_TARGET_HK1,
    ECO_TEMPERATURE_TARGET_HK1,
    COMFORT_TEMPERATURE_TARGET_HK2,
    ECO_TEMPERATURE_TARGET_HK2,
    COMFORT_TEMPERATURE_TARGET_HK3,
    ECO_TEMPERATURE_TARGET_HK3,
    OPERATION_MODE,
    FAN_LEVEL_DAY,
    FAN_LEVEL_NIGHT,
)
from .entity import StiebelEltronISGEntity

_LOGGER = logging.getLogger(__name__)

CLIMATE_HK_1 = "climate_hk_1"
CLIMATE_HK_2 = "climate_hk_2"
CLIMATE_HK_3 = "climate_hk_3"

ECO_MODE = 4

WPM_TO_HA_HVAC = {
    1: HVACMode.AUTO,
    2: HVACMode.AUTO,
    3: HVACMode.AUTO,
    4: HVACMode.AUTO,
    5: HVACMode.OFF,
    0: HVACMode.AUTO,
}

PRESET_PROGRAM = "program"
PRESET_WATER_HEATING = "water_heating"
PRESET_EMERGENCY = "emergency"
PRESET_READY = "ready"
PRESET_MANUAL = "manual"
PRESET_AUTO = "auto"


WPM_TO_HA_PRESET = {
    1: PRESET_READY,
    2: PRESET_PROGRAM,
    3: PRESET_COMFORT,
    4: PRESET_ECO,
    5: PRESET_WATER_HEATING,
    0: PRESET_EMERGENCY,
}

HA_TO_WPM_PRESET = {
    PRESET_READY: 1,
    PRESET_PROGRAM: 2,
    PRESET_COMFORT: 3,
    PRESET_ECO: 4,
    PRESET_WATER_HEATING: 5,
    PRESET_EMERGENCY: 0,
}

HA_TO_WPM_HVAC = {
    HVACMode.AUTO: 2,
    HVACMode.OFF: 5,
}

LWZ_TO_HA_HVAC = {
    11: HVACMode.AUTO,
    14: HVACMode.HEAT,
    1: HVACMode.AUTO,
    3: HVACMode.AUTO,
    4: HVACMode.AUTO,
    5: HVACMode.OFF,
    0: HVACMode.AUTO,
}

HA_TO_LWZ_HVAC = {
    HVACMode.AUTO: 11,
    HVACMode.OFF: 5,
    HVACMode.HEAT: 14,
}

LWZ_TO_HA_PRESET = {
    1: PRESET_READY,
    3: PRESET_COMFORT,
    4: PRESET_ECO,
    5: PRESET_WATER_HEATING,
    11: PRESET_AUTO,
    14: PRESET_MANUAL,
    0: PRESET_EMERGENCY,
}

HA_TO_LWZ_PRESET = {
    PRESET_READY: 1,
    PRESET_COMFORT: 3,
    PRESET_ECO: 4,
    PRESET_WATER_HEATING: 5,
    PRESET_AUTO: 11,
    PRESET_MANUAL: 14,
    PRESET_EMERGENCY: 0,
}

LWZ_TO_HA_FAN = {0: FAN_OFF, 1: FAN_LOW, 2: FAN_MEDIUM, 3: FAN_HIGH}
HA_TO_LWZ_FAN = {k: i for i, k in LWZ_TO_HA_FAN.items()}


CLIMATE_TYPES = [
    ClimateEntityDescription(CLIMATE_HK_1, has_entity_name=True, name="Heat Circuit 1"),
    ClimateEntityDescription(CLIMATE_HK_2, has_entity_name=True, name="Heat Circuit 2"),
    ClimateEntityDescription(CLIMATE_HK_3, has_entity_name=True, name="Heat Circuit 3"),
]

TEMPERATURE_KEY_MAP = {
    CLIMATE_HK_1: [ECO_TEMPERATURE_TARGET_HK1, COMFORT_TEMPERATURE_TARGET_HK1, 'sensor.node_1_network_analog_7'],
    CLIMATE_HK_2: [ECO_TEMPERATURE_TARGET_HK2, COMFORT_TEMPERATURE_TARGET_HK2, 'sensor.node_1_network_analog_8'],
    CLIMATE_HK_3: [ECO_TEMPERATURE_TARGET_HK3, COMFORT_TEMPERATURE_TARGET_HK3, 'sensor.node_1_network_analog_9'],
}

async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for description in CLIMATE_TYPES:
        climate_entity = (
            StiebelEltronWPMClimateEntity(coordinator, entry, description)
        )
        entities.append(climate_entity)
    async_add_devices(entities)


class StiebelEltronISGClimateEntity(StiebelEltronISGEntity, ClimateEntity):
    """stiebel_eltron_isg climate class."""

    def __init__(self, coordinator, config_entry, description):
        """Initialize the climate entity."""
        self.entity_description = description
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS

        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
        )
        self._attr_target_temperature_low = 5
        self._attr_target_temperature_high = 30
        self._attr_target_temperature_step = 0.1
        self._attr_translation_key = "climate"

        super().__init__(coordinator, config_entry)

    @property
    def unique_id(self) -> str | None:
        """Return the unique id of the climate entity."""
        return f"{DOMAIN}_{self.coordinator.name}_{self.entity_description.key}"

    @property
    def current_humidity(self) -> int | None:
        """Return the current humidity."""
        return self.coordinator.data.get(ACTUAL_HUMIDITY)

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        my_state = self.coordinator.hass.states.get(TEMPERATURE_KEY_MAP[self.entity_description.key][2])
        return (
            float(my_state.state)
            if my_state is not None
            else self.coordinator.data.get(ACTUAL_TEMPERATURE_FEK)
        )

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        if self.coordinator.data.get(OPERATION_MODE) == ECO_MODE:
            return self.coordinator.data.get(
                TEMPERATURE_KEY_MAP[self.entity_description.key][0]
            )
        else:
            return self.coordinator.data.get(
                TEMPERATURE_KEY_MAP[self.entity_description.key][1]
            )

    def set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        value = kwargs["temperature"]
        if self.coordinator.data.get(OPERATION_MODE) == ECO_MODE:
            self.coordinator.set_data(
                TEMPERATURE_KEY_MAP[self.entity_description.key][0], value
            )
        else:
            self.coordinator.set_data(
                TEMPERATURE_KEY_MAP[self.entity_description.key][1], value
            )

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added.

        This only applies when fist added to the entity registry.
        """
        return (
            self.coordinator.data.get(
                TEMPERATURE_KEY_MAP[self.entity_description.key][0]
            )
            is not None
        )


class StiebelEltronWPMClimateEntity(StiebelEltronISGClimateEntity):
    """stiebel_eltron_isg climate class for wpm."""

    def __init__(self, coordinator, config_entry, description):
        """Initialize the climate entity."""
        self._attr_hvac_modes = [HVACMode.AUTO, HVACMode.OFF]
        self._attr_preset_modes = [
            PRESET_READY,
            PRESET_PROGRAM,
            PRESET_ECO,
            PRESET_COMFORT,
            PRESET_WATER_HEATING,
            PRESET_EMERGENCY,
        ]
        super().__init__(coordinator, config_entry, description)

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return current operation ie. heat, cool, idle."""
        return WPM_TO_HA_HVAC.get(self.coordinator.data.get(OPERATION_MODE))

    def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new operation mode."""
        new_mode = HA_TO_WPM_HVAC.get(hvac_mode)
        self.coordinator.set_data(OPERATION_MODE, new_mode)

    @property
    def preset_mode(self) -> str | None:
        """Return current preset mode."""
        return WPM_TO_HA_PRESET.get(self.coordinator.data.get(OPERATION_MODE))

    def set_preset_mode(self, preset_mode):
        """Set new target preset mode."""
        new_mode = HA_TO_WPM_PRESET.get(preset_mode)
        self.coordinator.set_data(OPERATION_MODE, new_mode)


