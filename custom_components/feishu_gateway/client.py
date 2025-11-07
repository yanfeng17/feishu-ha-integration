"""Client helper to interact with the external Feishu gateway service."""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
from typing import Any, Dict

from aiohttp import ClientError, ClientSession, WSMsgType
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import EVENT_MESSAGE, SIGNAL_NEW_MESSAGE

_LOGGER = logging.getLogger(__name__)


class FeishuGatewayClient:
    """Manage HTTP and WebSocket interactions with the gateway service."""

    def __init__(self, hass: HomeAssistant, base_url: str, access_token: str | None) -> None:
        self.hass = hass
        self._session: ClientSession = aiohttp_client.async_get_clientsession(hass)
        self._base_url = base_url.rstrip("/")
        self._token = access_token
        self._listener_task: asyncio.Task | None = None
        self._stopping = asyncio.Event()

    async def async_start(self) -> None:
        if self._listener_task:
            return
        if self._stopping.is_set():
            self._stopping = asyncio.Event()
        self._listener_task = self.hass.loop.create_task(self._listen_loop())

    async def async_stop(self) -> None:
        self._stopping.set()
        if self._listener_task:
            self._listener_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._listener_task
            self._listener_task = None

    async def async_send_text(self, target: str, content: str, at_list: list[str] | None = None) -> None:
        url = f"{self._base_url}/send_message"
        headers = self._build_headers()
        payload: Dict[str, Any] = {"target": target, "content": content}
        if at_list:
            payload["at_list"] = at_list
        try:
            async with self._session.post(url, json=payload, headers=headers, timeout=15) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise HomeAssistantError(f"Gateway send_message failed: {resp.status} {text}")
        except ClientError as exc:
            raise HomeAssistantError(f"Failed to reach gateway: {exc}") from exc

    async def _listen_loop(self) -> None:
        """WebSocket listener with exponential backoff retry."""
        url = f"{self._base_url}/ws"
        headers = self._build_headers()
        retry_delay = 1  # Start with 1 second
        max_retry_delay = 60  # Max 60 seconds
        
        while not self._stopping.is_set():
            try:
                _LOGGER.debug("Connecting to Gateway WebSocket: %s", url)
                async with self._session.ws_connect(
                    url, heartbeat=30, headers=headers, timeout=10
                ) as ws:
                    _LOGGER.info("Gateway WebSocket connected")
                    retry_delay = 1  # Reset retry delay on successful connection
                    
                    async for msg in ws:
                        if msg.type == WSMsgType.TEXT:
                            try:
                                data = json.loads(msg.data)
                                self._handle_event(data)
                            except json.JSONDecodeError as err:
                                _LOGGER.error("Failed to decode message: %s", err)
                        elif msg.type == WSMsgType.ERROR:
                            _LOGGER.warning("WebSocket error, will reconnect")
                            break
                        elif msg.type == WSMsgType.CLOSED:
                            _LOGGER.info("WebSocket closed by server")
                            break
                            
            except ClientError as err:
                if not self._stopping.is_set():
                    _LOGGER.warning(
                        "Gateway connection failed: %s, retrying in %ds",
                        err,
                        retry_delay,
                    )
                    await asyncio.sleep(retry_delay)
                    # Exponential backoff
                    retry_delay = min(retry_delay * 2, max_retry_delay)
            except Exception as err:
                if not self._stopping.is_set():
                    _LOGGER.exception("Unexpected error in WebSocket loop: %s", err)
                    await asyncio.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, max_retry_delay)

    def _handle_event(self, data: Dict[str, Any]) -> None:
        """Handle incoming message event and dispatch to listeners."""
        try:
            # Fire event to event bus (for automations)
            self.hass.bus.async_fire(EVENT_MESSAGE, data)
            # Send signal to dispatcher (for sensors) - this is faster
            async_dispatcher_send(self.hass, SIGNAL_NEW_MESSAGE, data)
            _LOGGER.debug("Message event dispatched: %s", data.get("content", "")[:50])
        except Exception as err:
            _LOGGER.error("Error handling event: %s", err)

    def _build_headers(self) -> Dict[str, str]:
        if not self._token:
            return {}
        return {"X-Access-Token": self._token}
