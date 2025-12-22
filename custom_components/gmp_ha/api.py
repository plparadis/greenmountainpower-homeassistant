"""API wrapper for GMP HA usage data."""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from functools import partial
from typing import List

import greenmountainpower.api as gmp_api
import oauthlib.oauth2
import requests_oauthlib
from homeassistant.core import HomeAssistant


@dataclass
class HourlyUsage:
    """A single hour of usage from Green Mountain Power."""

    start_time: datetime.datetime
    consumed_kwh: float


class GmpClient:
    """Client wrapper around the greenmountainpower library."""

    hass: HomeAssistant
    api: gmp_api.GreenMountainPowerApi

    @classmethod
    async def create(
        cls, hass: HomeAssistant, account_number: int, username: str, password: str
    ) -> "GmpClient":
        """Create a GMP client in the executor."""

        api = await hass.async_add_executor_job(
            partial(_create_gmp_api, account_number, username, password)
        )
        return cls(hass=hass, api=api)

    async def async_get_account_status(self):
        """Get the account status via the executor."""

        return await self.hass.async_add_executor_job(self.api.get_account_status)

    async def async_get_hourly_usage(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> List[HourlyUsage]:
        """Return hourly usage data between the provided timestamps."""

        usages = await self.hass.async_add_executor_job(
            self.api.get_usage,
            gmp_api.UsagePrecision.HOURLY,
            start,
            end,
        )
        return [
            HourlyUsage(start_time=usage.start_time, consumed_kwh=usage.consumed_kwh)
            for usage in usages
        ]


def _create_gmp_api(
    account_number: int, username: str, password: str
) -> gmp_api.GreenMountainPowerApi:
    """Create a GMP API client without embedding credentials in the query string."""

    api = gmp_api.GreenMountainPowerApi.__new__(gmp_api.GreenMountainPowerApi)
    api.account_number = account_number

    def token_updater(token):
        api.session.token = token

    api.session = requests_oauthlib.OAuth2Session(
        client=oauthlib.oauth2.LegacyApplicationClient(client_id=gmp_api._CLIENT_ID),
        auto_refresh_url=f"{gmp_api._BASE_URL}/api/v2/applications/token",
        token_updater=token_updater,
    )
    api.session.fetch_token(
        token_url=f"{gmp_api._BASE_URL}/api/v2/applications/token",
        username=username,
        password=password,
        include_client_id=True,
    )

    return api
