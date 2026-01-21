"""Integration setup for GMP HA."""
from __future__ import annotations

import logging
from datetime import datetime
from datetime import timedelta

from greenmountainpower import exceptions as gmp_exceptions
from greenmountainpower.api import UsagePrecision
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import dt as dt_util

from .api import GmpClient
from .api import HourlyUsage
from .const import CONF_ACCOUNT_NUMBER
from .const import CONF_BACKFILL_DAYS
from .const import CONF_PASSWORD
from .const import CONF_PRICE_PER_KWH
from .const import CONF_USERNAME
from .const import DEFAULT_BACKFILL_DAYS
from .const import DEFAULT_PRICE_PER_KWH
from .const import DOMAIN
from .const import HOURLY_AVAILABILITY_DELAY_HOURS
from .const import HOURLY_LOOKBACK_HOURS
from .const import NAME
from .const import PLATFORMS
from .const import SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up GMP HA from a config entry."""

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

    client = await GmpClient.create(
        hass,
        account_number=account_number,
        username=username,
        password=password,
    )

    coordinator = GmpHaCoordinator(
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


class GmpHaCoordinator(DataUpdateCoordinator):
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
        self._backfill_days = backfill_days
        self._usage_history: list[HourlyUsage] = []
        self._refresh_window = timedelta(hours=1)
        self._lookback_window = timedelta(hours=HOURLY_LOOKBACK_HOURS)
        self._availability_delay = timedelta(hours=HOURLY_AVAILABILITY_DELAY_HOURS)
        self._total_kwh: float | None = None

        now = dt_util.as_utc(dt_util.now())
        self._start_time = now - timedelta(days=backfill_days)

        super().__init__(
            hass,
            _LOGGER,
            name=NAME,  # noqa: WPS317
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch usage data from the API."""

        end = dt_util.as_utc(dt_util.now())
        monthly_start = end - timedelta(days=62)
        daily_start = monthly_start
        window_start = end - timedelta(days=self._backfill_days)
        missing_window_end = _floor_hour(end - self._availability_delay)
        missing_window_start = max(
            window_start, missing_window_end - self._lookback_window
        )
        missing_hours = _find_missing_hours(
            self._usage_history, missing_window_start, missing_window_end
        )

        try:
            if not self._usage_history:
                hourly_start = self._start_time
            elif missing_hours:
                hourly_start = missing_hours[0]
            else:
                hourly_start = end - self._refresh_window

            new_usages = await self.client.async_get_usage(
                UsagePrecision.HOURLY, hourly_start, end
            )
            daily_usage = await self.client.async_get_usage(
                UsagePrecision.DAILY, daily_start, end
            )
            monthly_usage = await self.client.async_get_usage(
                UsagePrecision.MONTHLY, monthly_start, end
            )
        except gmp_exceptions.UnauthorizedException as err:
            raise ConfigEntryAuthFailed from err
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(err) from err

        self._usage_history, total_delta = _merge_usage(self._usage_history, new_usages)
        self._usage_history = [
            usage for usage in self._usage_history if usage.start_time >= window_start
        ]
        missing_hours = _find_missing_hours(
            self._usage_history, missing_window_start, missing_window_end
        )

        usages = self._usage_history
        if self._total_kwh is None:
            self._total_kwh = sum(usage.consumed_kwh for usage in usages)
        else:
            self._total_kwh += total_delta
        total_kwh = self._total_kwh
        today = dt_util.now().date()
        today_kwh = sum(
            usage.consumed_kwh
            for usage in usages
            if dt_util.as_local(dt_util.as_utc(usage.start_time)).date() == today
        )
        yesterday = today - timedelta(days=1)
        yesterday_kwh = _find_daily_value(daily_usage, yesterday)
        latest_usage = max(usages, key=lambda usage: usage.start_time, default=None)
        current_hour_start = latest_usage.start_time if latest_usage else None
        previous_hour_start = (
            current_hour_start - timedelta(hours=1)
            if current_hour_start is not None
            else None
        )
        current_hour_usage = latest_usage
        previous_hour_usage = (
            _find_usage_at(usages, previous_hour_start)
            if previous_hour_start is not None
            else None
        )
        current_hour = (
            current_hour_usage.consumed_kwh if current_hour_usage is not None else None
        )
        previous_hour = (
            previous_hour_usage.consumed_kwh
            if previous_hour_usage is not None
            else None
        )
        hourly_trend = _trend(current_hour, previous_hour)
        daily_trend = _trend(today_kwh, yesterday_kwh)

        current_month = (end.year, end.month)
        previous_month = _previous_month(end)
        current_month_kwh = _find_monthly_value(monthly_usage, current_month)
        previous_month_kwh = _find_monthly_value(monthly_usage, previous_month)
        month_start = dt_util.as_local(end).date().replace(day=1)
        previous_month_start = month_start.replace(day=1) - timedelta(days=1)
        previous_month_start = previous_month_start.replace(day=1)
        month_to_date_kwh = _sum_usage_between(
            daily_usage, month_start, dt_util.as_local(end).date()
        )
        previous_month_to_date_kwh = _sum_usage_between(
            daily_usage,
            previous_month_start,
            _month_to_date_end(previous_month_start, end.day),
        )
        month_to_date_trend = _trend(month_to_date_kwh, previous_month_to_date_kwh)
        estimated_cost = (
            round(current_month_kwh * self.price_per_kwh, 2)
            if current_month_kwh is not None
            else round(total_kwh * self.price_per_kwh, 2)
        )
        previous_bill = (
            round(previous_month_kwh * self.price_per_kwh, 2)
            if previous_month_kwh is not None
            else None
        )

        return {
            "total_kwh": round(total_kwh, 3),
            "today_kwh": round(today_kwh, 3),
            "estimated_cost": estimated_cost,
            "yesterday_kwh": _round_or_none(yesterday_kwh),
            "current_hour_kwh": _round_or_none(current_hour),
            "previous_hour_kwh": _round_or_none(previous_hour),
            "current_hour_start": (
                current_hour_usage.start_time
                if current_hour_usage is not None
                else None
            ),
            "previous_hour_start": (
                previous_hour_usage.start_time
                if previous_hour_usage is not None
                else None
            ),
            "hourly_trend": _round_or_none(hourly_trend),
            "daily_trend": _round_or_none(daily_trend),
            "month_to_date_kwh": _round_or_none(month_to_date_kwh),
            "previous_month_to_date_kwh": _round_or_none(previous_month_to_date_kwh),
            "month_to_date_trend": _round_or_none(month_to_date_trend),
            "current_month_kwh": _round_or_none(current_month_kwh),
            "previous_month_kwh": _round_or_none(previous_month_kwh),
            "previous_bill": previous_bill,
            "missing_hour_count": len(missing_hours),
            "missing_hours": [
                dt_util.as_local(hour).isoformat() for hour in missing_hours
            ],
            "missing_hours_window_start": (
                dt_util.as_local(missing_window_start).isoformat()
                if missing_window_start is not None
                else None
            ),
            "missing_hours_window_end": (
                dt_util.as_local(missing_window_end).isoformat()
                if missing_window_end is not None
                else None
            ),
            "usages": usages,
        }


def _merge_usage(
    existing: list[HourlyUsage], new_values: list[HourlyUsage]
) -> tuple[list[HourlyUsage], float]:
    if not existing:
        return sorted(new_values, key=lambda usage: usage.start_time), sum(
            usage.consumed_kwh for usage in new_values
        )

    combined = {usage.start_time: usage for usage in existing}
    delta = 0.0
    for usage in new_values:
        if usage.start_time in combined:
            delta += usage.consumed_kwh - combined[usage.start_time].consumed_kwh
        else:
            delta += usage.consumed_kwh
        combined[usage.start_time] = usage
    return sorted(combined.values(), key=lambda usage: usage.start_time), delta


def _find_daily_value(usages: list[HourlyUsage], target_date):
    for usage in usages:
        if dt_util.as_local(dt_util.as_utc(usage.start_time)).date() == target_date:
            return usage.consumed_kwh
    return None


def _find_usage_at(
    usages: list[HourlyUsage], start_time: datetime
) -> HourlyUsage | None:
    if not usages:
        return None
    usage_by_start = {usage.start_time: usage for usage in usages}
    return usage_by_start.get(start_time)


def _trend(current: float | None, previous: float | None):
    if current is None or previous is None:
        return None
    return current - previous


def _find_monthly_value(usages: list[HourlyUsage], target_month: tuple[int, int]):
    if target_month is None:
        return None
    for usage in usages:
        if (usage.start_time.year, usage.start_time.month) == target_month:
            return usage.consumed_kwh
    return None


def _sum_usage_between(usages: list[HourlyUsage], start_date, end_date) -> float | None:
    if not usages:
        return None

    total = 0.0
    for usage in usages:
        usage_date = dt_util.as_local(dt_util.as_utc(usage.start_time)).date()
        if start_date <= usage_date <= end_date:
            total += usage.consumed_kwh

    return total if total > 0 else 0.0


def _month_to_date_end(previous_month_start, current_day_of_month):
    last_day_previous_month = previous_month_start.replace(day=1) + timedelta(days=32)
    last_day_previous_month = last_day_previous_month.replace(day=1) - timedelta(days=1)
    days_to_include = min(current_day_of_month, last_day_previous_month.day)
    return previous_month_start + timedelta(days=days_to_include - 1)


def _previous_month(date_time):
    month = date_time.month - 1 or 12
    year = date_time.year - 1 if month == 12 else date_time.year
    return year, month


def _round_or_none(value: float | None, digits: int = 3):
    if value is None:
        return None
    return round(value, digits)


def _floor_hour(value: datetime) -> datetime:
    return value.replace(minute=0, second=0, microsecond=0)


def _find_missing_hours(
    usages: list[HourlyUsage], start_time: datetime, end_time: datetime
) -> list[datetime]:
    if start_time >= end_time:
        return []

    usage_by_start = {usage.start_time: usage for usage in usages}
    missing: list[datetime] = []
    current = start_time
    while current < end_time:
        if current not in usage_by_start:
            missing.append(current)
        current += timedelta(hours=1)
    return missing
