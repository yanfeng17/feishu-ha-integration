"""Sensor platform for the Feishu Gateway integration."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DATA_CLIENT, DOMAIN, SIGNAL_NEW_MESSAGE


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    entity = FeishuLastMessageSensor(entry.entry_id)
    async_add_entities([entity])

    # Use async callback for better performance
    async def async_handle_event(data: Dict[str, Any]) -> None:
        await entity.async_handle_new_message(data)

    remove = async_dispatcher_connect(hass, SIGNAL_NEW_MESSAGE, async_handle_event)

    async def async_remove_listener() -> None:
        remove()

    hass.data[DOMAIN][entry.entry_id]["remove_listener"] = async_remove_listener


class FeishuLastMessageSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, entry_id: str) -> None:
        self._attr_unique_id = f"{entry_id}_last_message"
        self._attr_name = "Feishu Last Message"
        self._attr_native_value = None
        self._attr_extra_state_attributes: Dict[str, Any] = {}

    async def async_handle_new_message(self, data: Dict[str, Any]) -> None:
        """Handle new message from Gateway (async for better performance)."""
        self._attr_native_value = data.get("content")
        self._attr_extra_state_attributes = {
            "sender": data.get("sender"),
            "sender_name": data.get("sender_name"),
            "room_id": data.get("room_id"),
            "room_name": data.get("room_name"),
            "timestamp": data.get("timestamp"),
            "received_at": datetime.utcnow().isoformat(),
        }
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        domain_data = self.hass.data.get(DOMAIN, {})
        entry_data = domain_data.get(self._extract_entry_id())
        if not entry_data:
            return
        remove_listener = entry_data.get("remove_listener")
        if remove_listener:
            await remove_listener()
            entry_data["remove_listener"] = None

    def _extract_entry_id(self) -> str:
        return self._attr_unique_id.replace("_last_message", "")
