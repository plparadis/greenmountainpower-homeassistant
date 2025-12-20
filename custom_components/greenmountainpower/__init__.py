"""Integration setup for Green Mountain Power."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import GmpClient
from .const import (
    CONF_ACCOUNT_NUMBER,
    CONF_BACKFILL_DAYS,
    CONF_PASSWORD,
    CONF_PRICE_PER_KWH,
    CONF_USERNAME,
    DEFAULT_BACKFILL_DAYS,
    DEFAULT_PRICE_PER_KWH,
    DOMAIN,
    PLATFORMS,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Green Mountain Power integration."""

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Green Mountain Power from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    account_number = entry.data[CONF_ACCOUNT_NUMBER]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    price_per_kwh = entry.options.get(
        CONF_PRICE_PER_KWH, entry.data.get(CONF_PRICE_PER_KWH, DEFAULT_PRICE_PER_KWH)
    )
    backfill_days = entry.options.get(
        CONF_BACKFILL_DAYS, entry.data.get(CONF_BACKFILL_DAYS, DEFAULT_BACKFILL_DAYS)
    )

    client = GmpClient(
        account_number=account_number,
        username=username,
        password=password,
    )

    coordinator = GreenMountainPowerCoordinator(
        hass,
        client=client,
        price_per_kwh=price_per_kwh,
        backfill_days=backfill_days,
    )

    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


class GreenMountainPowerCoordinator(DataUpdateCoordinator):
    """Coordinator to retrieve usage data from Green Mountain Power."""

    def __init__(
        self,
        hass: HomeAssistant,
        *,
        client: GmpClient,
        price_per_kwh: float,
        backfill_days: int,
    ) -> None:
        self.client = client
        self.price_per_kwh = price_per_kwh
        self.backfill_days = backfill_days

        super().__init__(
            hass,
            _LOGGER,
            name="Green Mountain Power",  # noqa: WPS317
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch usage data from the API."""

        start = dt_util.utcnow() - timedelta(days=self.backfill_days)
        end = dt_util.utcnow()

        try:
            usages = await self.hass.async_add_executor_job(
                self.client.get_hourly_usage, start, end
            )
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(err) from err

        total_kwh = sum(usage.consumed_kwh for usage in usages)
        today = dt_util.as_local(dt_util.utcnow()).date()
        today_kwh = sum(
            usage.consumed_kwh
            for usage in usages
            if dt_util.as_local(dt_util.as_utc(usage.start_time)).date() == today
        )
        estimated_cost = total_kwh * self.price_per_kwh

        return {
            "total_kwh": round(total_kwh, 3),
            "today_kwh": round(today_kwh, 3),
            "estimated_cost": round(estimated_cost, 2),
            "usages": usages,
        }
