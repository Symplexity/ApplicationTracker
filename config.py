"""
Configuration settings for the discord bot. Maintains shared constants and settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()
_DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
assert _DISCORD_TOKEN is not None, "DISCORD_TOKEN is required"
DISCORD_TOKEN = _DISCORD_TOKEN
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
COMMAND_PREFIX = "!"
