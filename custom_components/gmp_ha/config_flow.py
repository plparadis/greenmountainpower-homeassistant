"""Config flow for the GMP HA integration."""
from __future__ import annotations

from datetime import timedelta

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util import dt as dt_util

from .api import GmpClient
from .const import CONF_ACCOUNT_NUMBER
from .const import CONF_BACKFILL_DAYS
from .const import CONF_PASSWORD
from .const import CONF_PRICE_PER_KWH
from .const import CONF_USERNAME
from .const import DEFAULT_BACKFILL_DAYS
from .const import DEFAULT_PRICE_PER_KWH
from .const import DOMAIN
from greenmountainpower import exceptions as gmp_exceptions


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GMP HA."""

    VERSION = 1

    def __init__(self) -> None:
        self._errors: dict[str, str] = {}

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""

        self._errors = {}

        if user_input is not None:
            try:
                await self._validate_input(user_input)
            except InvalidAuth:
                self._errors["base"] = "invalid_auth"
            except CannotConnect:
                self._errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                self._errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(str(user_input[CONF_ACCOUNT_NUMBER]))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=str(user_input[CONF_ACCOUNT_NUMBER]),
                    data=user_input,
                )

        return self._show_form(user_input)

    def _show_form(self, user_input):
        defaults = user_input or {}
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ACCOUNT_NUMBER, default=defaults.get(CONF_ACCOUNT_NUMBER)
                    ): vol.Coerce(int),
                    vol.Required(
                        CONF_USERNAME, default=defaults.get(CONF_USERNAME, "")
                    ): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(
                        CONF_PRICE_PER_KWH,
                        default=defaults.get(CONF_PRICE_PER_KWH, DEFAULT_PRICE_PER_KWH),
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_BACKFILL_DAYS,
                        default=defaults.get(CONF_BACKFILL_DAYS, DEFAULT_BACKFILL_DAYS),
                    ): vol.Coerce(int),
                }
            ),
            errors=self._errors,
        )

    async def _validate_input(self, user_input: dict):
        """Validate the user input allows us to connect."""

        client = GmpClient(
            account_number=int(user_input[CONF_ACCOUNT_NUMBER]),
            username=user_input[CONF_USERNAME],
            password=user_input[CONF_PASSWORD],
        )

        start = dt_util.utcnow() - timedelta(days=1)
        end = dt_util.utcnow()

        try:
            await self.hass.async_add_executor_job(client.get_hourly_usage, start, end)
        except gmp_exceptions.UnauthorizedException as err:
            raise InvalidAuth from err
        except Exception as err:  # noqa: BLE001
            raise CannotConnect from err

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """Handle options for GMP HA."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Options", data=user_input)

        data = {**self.config_entry.data, **self.config_entry.options}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_PRICE_PER_KWH,
                        default=data.get(CONF_PRICE_PER_KWH, DEFAULT_PRICE_PER_KWH),
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_BACKFILL_DAYS,
                        default=data.get(CONF_BACKFILL_DAYS, DEFAULT_BACKFILL_DAYS),
                    ): vol.Coerce(int),
                }
            ),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
