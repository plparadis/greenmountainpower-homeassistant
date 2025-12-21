"""Sensor platform for the Green Mountain Power integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfCurrency
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import GreenMountainPowerEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Green Mountain Power sensors based on a config entry."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            GmpGridEnergySensor(coordinator, entry.entry_id),
            GmpDailyEnergySensor(coordinator, entry.entry_id),
            GmpEstimatedBillSensor(coordinator, entry.entry_id),
        ]
    )


class GmpGridEnergySensor(GreenMountainPowerEntity, SensorEntity):
    """Total energy used from the grid."""

    _attr_translation_key = "grid_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="grid_energy")

    @property
    def native_value(self):
        return self.coordinator.data["total_kwh"]


class GmpDailyEnergySensor(GreenMountainPowerEntity, SensorEntity):
    """Energy used today."""

    _attr_translation_key = "daily_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="daily_energy")

    @property
    def native_value(self):
        return self.coordinator.data["today_kwh"]


class GmpEstimatedBillSensor(GreenMountainPowerEntity, SensorEntity):
    """Estimated cost for the current period."""

    _attr_translation_key = "estimated_bill"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfCurrency.USD

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="estimated_bill")

    @property
    def native_value(self):
        return self.coordinator.data["estimated_cost"]
