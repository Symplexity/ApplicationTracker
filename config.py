"""
Configuration settings for the discord bot. Maintains shared constants and settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()
_DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
assert _DISCORD_TOKEN is not None, "DISCORD_TOKEN is required"
DISCORD_TOKEN = _DISCORD_TOKEN
_CLIENT_ID = os.getenv("CLIENT_ID")
assert _CLIENT_ID is not None, "CLIENT_ID is required"
CLIENT_ID = _CLIENT_ID
COMMAND_PREFIX = "!"

__debug = False


def set_debug(debug: bool) -> None:
    """Sets the debug mode for the bot."""
    global __debug
    __debug = debug


def get_debug() -> bool:
    """Gets the current debug mode for the bot."""
    return __debug
