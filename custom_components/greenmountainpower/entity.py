"""Base entity for Green Mountain Power sensors."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .const import NAME


class GreenMountainPowerEntity(CoordinatorEntity):
    """Representation of a Green Mountain Power entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry_id: str, *, unique_suffix: str) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._unique_suffix = unique_suffix

    @property
    def unique_id(self) -> str:
        return f"{self._entry_id}_{self._unique_suffix}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": NAME,
            "manufacturer": NAME,
        }
