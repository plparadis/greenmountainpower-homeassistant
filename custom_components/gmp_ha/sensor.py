"""Sensor platform for the GMP HA integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .entity import GmpHaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GMP HA sensors based on a config entry."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            GmpGridEnergySensor(coordinator, entry.entry_id),
            GmpDailyEnergySensor(coordinator, entry.entry_id),
            GmpEstimatedBillSensor(coordinator, entry.entry_id),
            GmpYesterdayEnergySensor(coordinator, entry.entry_id),
            GmpCurrentHourEnergySensor(coordinator, entry.entry_id),
            GmpPreviousHourEnergySensor(coordinator, entry.entry_id),
            GmpHourlyTrendSensor(coordinator, entry.entry_id),
            GmpDailyTrendSensor(coordinator, entry.entry_id),
            GmpCurrentMonthEnergySensor(coordinator, entry.entry_id),
            GmpPreviousMonthEnergySensor(coordinator, entry.entry_id),
            GmpMonthToDateEnergySensor(coordinator, entry.entry_id),
            GmpPreviousMonthToDateEnergySensor(coordinator, entry.entry_id),
            GmpMonthToDateTrendSensor(coordinator, entry.entry_id),
            GmpPreviousBillSensor(coordinator, entry.entry_id),
        ]
    )


class GmpGridEnergySensor(GmpHaEntity, SensorEntity):
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


class GmpDailyEnergySensor(GmpHaEntity, SensorEntity):
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


class GmpYesterdayEnergySensor(GmpHaEntity, SensorEntity):
    """Energy used yesterday."""

    _attr_translation_key = "yesterday_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="yesterday_energy")

    @property
    def native_value(self):
        return self.coordinator.data["yesterday_kwh"]


class GmpCurrentHourEnergySensor(GmpHaEntity, SensorEntity):
    """Energy used in the current hour."""

    _attr_translation_key = "current_hour_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="current_hour_energy")

    @property
    def native_value(self):
        return self.coordinator.data["current_hour_kwh"]

    @property
    def last_reset(self):
        start = self.coordinator.data["current_hour_start"]
        if start is None:
            return None
        return dt_util.as_utc(start)

    @property
    def extra_state_attributes(self):
        start = self.coordinator.data["current_hour_start"]
        if start is None:
            return None
        return {
            "start_time": dt_util.as_local(start).isoformat(),
            "end_time": (dt_util.as_local(start) + timedelta(hours=1)).isoformat(),
        }


class GmpPreviousHourEnergySensor(GmpHaEntity, SensorEntity):
    """Energy used in the previous hour."""

    _attr_translation_key = "previous_hour_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="previous_hour_energy")

    @property
    def native_value(self):
        return self.coordinator.data["previous_hour_kwh"]

    @property
    def last_reset(self):
        start = self.coordinator.data["previous_hour_start"]
        if start is None:
            return None
        return dt_util.as_utc(start)

    @property
    def extra_state_attributes(self):
        start = self.coordinator.data["previous_hour_start"]
        if start is None:
            return None
        return {
            "start_time": dt_util.as_local(start).isoformat(),
            "end_time": (dt_util.as_local(start) + timedelta(hours=1)).isoformat(),
        }


class GmpHourlyTrendSensor(GmpHaEntity, SensorEntity):
    """Difference between the current and previous hour usage."""

    _attr_translation_key = "hourly_trend"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="hourly_trend")

    @property
    def native_value(self):
        return self.coordinator.data["hourly_trend"]


class GmpDailyTrendSensor(GmpHaEntity, SensorEntity):
    """Difference between today and yesterday usage."""

    _attr_translation_key = "daily_trend"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="daily_trend")

    @property
    def native_value(self):
        return self.coordinator.data["daily_trend"]


class GmpCurrentMonthEnergySensor(GmpHaEntity, SensorEntity):
    """Energy used in the current month."""

    _attr_translation_key = "current_month_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="current_month_energy")

    @property
    def native_value(self):
        return self.coordinator.data["current_month_kwh"]


class GmpPreviousMonthEnergySensor(GmpHaEntity, SensorEntity):
    """Energy used in the previous month."""

    _attr_translation_key = "previous_month_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="previous_month_energy")

    @property
    def native_value(self):
        return self.coordinator.data["previous_month_kwh"]


class GmpMonthToDateEnergySensor(GmpHaEntity, SensorEntity):
    """Energy used so far this month."""

    _attr_translation_key = "month_to_date_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="month_to_date_energy")

    @property
    def native_value(self):
        return self.coordinator.data["month_to_date_kwh"]


class GmpPreviousMonthToDateEnergySensor(GmpHaEntity, SensorEntity):
    """Energy used at the same point last month."""

    _attr_translation_key = "previous_month_to_date_energy"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(
            coordinator, entry_id, unique_suffix="previous_month_to_date_energy"
        )

    @property
    def native_value(self):
        return self.coordinator.data["previous_month_to_date_kwh"]


class GmpMonthToDateTrendSensor(GmpHaEntity, SensorEntity):
    """Difference between current and prior month-to-date usage."""

    _attr_translation_key = "month_to_date_trend"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="month_to_date_trend")

    @property
    def native_value(self):
        return self.coordinator.data["month_to_date_trend"]


class GmpPreviousBillSensor(GmpHaEntity, SensorEntity):
    """Cost of the previous month based on configured pricing."""

    _attr_translation_key = "previous_bill"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = "USD"

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="previous_bill")

    @property
    def native_value(self):
        return self.coordinator.data["previous_bill"]


class GmpEstimatedBillSensor(GmpHaEntity, SensorEntity):
    """Estimated cost for the current period."""

    _attr_translation_key = "estimated_bill"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = "USD"

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, unique_suffix="estimated_bill")

    @property
    def native_value(self):
        return self.coordinator.data["estimated_cost"]
