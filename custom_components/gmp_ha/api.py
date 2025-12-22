"""API wrapper for GMP HA usage data."""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List

import greenmountainpower


@dataclass
class HourlyUsage:
    """A single hour of usage from Green Mountain Power."""

    start_time: datetime.datetime
    consumed_kwh: float


class GmpClient:
    """Client wrapper around the greenmountainpower library."""

    def __init__(self, account_number: int, username: str, password: str) -> None:
        self._api = greenmountainpower.api.GreenMountainPowerApi(
            account_number=account_number,
            username=username,
            password=password,
        )

    def get_hourly_usage(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> List[HourlyUsage]:
        """Return hourly usage data between the provided timestamps."""

        usages = self._api.get_usage(
            precision=greenmountainpower.api.UsagePrecision.HOURLY,
            start_time=start,
            end_time=end,
        )
        return [
            HourlyUsage(start_time=usage.start_time, consumed_kwh=usage.consumed_kwh)
            for usage in usages
        ]
