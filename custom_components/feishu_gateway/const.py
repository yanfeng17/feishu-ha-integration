"""Constants for the Feishu Gateway integration."""

from homeassistant.const import Platform


DOMAIN = "feishu_gateway"

CONF_BASE_URL = "base_url"
CONF_ACCESS_TOKEN = "access_token"

DATA_CLIENT = "client"

EVENT_MESSAGE = "feishu_gateway_message"
SIGNAL_NEW_MESSAGE = "feishu_gateway_new_message"

# Service names
SERVICE_SEND_MESSAGE = "send_message"
SERVICE_SEND_IMAGE = "send_image"

PLATFORMS = [Platform.SENSOR]
