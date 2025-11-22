"""
Configuration settings for the discord bot. Maintains shared constants and settings.
"""

import os
from dotenv import load_dotenv
from configparser import ConfigParser

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


def config(filename="database.ini", section="postgres"):
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section, default to postgres
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return db
