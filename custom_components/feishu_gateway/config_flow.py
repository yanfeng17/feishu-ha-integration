"""Config flow for Feishu Gateway integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_ACCESS_TOKEN, CONF_BASE_URL, DOMAIN


class FeishuGatewayConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Feishu Gateway."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_BASE_URL): str,
                        vol.Optional(CONF_ACCESS_TOKEN): str,
                    }
                ),
            )

        await self.async_set_unique_id(user_input[CONF_BASE_URL])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title="Feishu Gateway", data=user_input)
