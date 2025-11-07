"""
Main entry point for the ApplicationTracker bot.
"""

import discord
import logging
import os
import sys
import argparse

from discord.ext import commands
from config import DISCORD_TOKEN, CLIENT_ID, COMMAND_PREFIX, set_debug, get_debug

# Parse command-line arguments
parser = argparse.ArgumentParser(description="ApplicationTracker Bot")
parser.add_argument("--debug", action="store_true", help="Run the bot in debug mode")
parser.add_argument(
    "--generate_invite",
    "--invite",
    "-g",
    action="store_true",
    help="Generate an invite link for the bot, then exit without starting the bot.",
)
args = parser.parse_args()

if args.generate_invite:
    permissions = discord.Permissions(permissions=8)  # Administrator permissions
    invite_url = discord.utils.oauth_url(CLIENT_ID, permissions=permissions)
    print(f"Invite link: {invite_url}")
    sys.exit(0)

set_debug(args.debug)
DEBUG = get_debug()

# Set up logging
logger = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


intents = discord.Intents.default()
# intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready() -> None:
    assert bot.user is not None
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    if DEBUG:
        logger.debug("Running in debug mode.")
        # Clear messages in the testing channel
        channel = discord.utils.get(bot.get_all_channels(), name="testing")
        if channel and isinstance(channel, discord.TextChannel):
            await channel.purge()
            logger.debug("Cleared messages in the testing channel.")
    else:
        logger.info("Running in production mode.")

    # Load cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith("_cog.py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                logger.info(f"Loaded cog: {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_name}: {e}")

    # Unload the test cog outside of debug mode
    if not DEBUG:
        try:
            await bot.unload_extension("cogs.test_cog")
            logger.info("Unloaded test_cog for production mode.")
        except Exception as e:
            logger.error(f"Failed to unload test_cog: {e}")

    logger.info(f"{bot.user.name} setup complete.")


if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error starting the bot: {e}")
