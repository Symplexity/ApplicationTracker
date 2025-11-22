"""
Main entry point for the ApplicationTracker bot.
"""

import discord
import logging
import os
import sys
import argparse
import psycopg

from discord.ext import commands
from app.config import (
    DISCORD_TOKEN,
    CLIENT_ID,
    COMMAND_PREFIX,
    TABLE_NAME,
    TABLE_LAYOUT,
    set_debug,
    get_debug,
    config,
)


class DataBaseBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize and test database connection
        self.conn = None
        try:
            params = config()
            print("Connecting to the PostgreSQL database...")
            self.conn = psycopg.connect(**params)
            print("Database connection successful.")

            cur = self.conn.cursor()
            print("PostgreSQL database version:")
            cur.execute("SELECT version()")
            db_version = cur.fetchone()
            print(db_version)
            cur.close()

            # Create table for tracked applications if it doesn't exist
            cur = self.conn.cursor()
            # cur.execute(
            #     """
            #     CREATE TABLE IF NOT EXISTS tracked_applications (
            #         id SERIAL PRIMARY KEY,
            #         name VARCHAR(255) UNIQUE NOT NULL,
            #         status VARCHAR(50) NOT NULL,
            #         applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            #         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            #     )
            #     """
            # )
            cur.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} {TABLE_LAYOUT}")
            self.conn.commit()
            cur.close()
        except (Exception, psycopg.DatabaseError) as error:
            print(f"Database connection error: {error}")
            sys.exit(1)


def _create_bot(debug: bool) -> DataBaseBot:
    """
    Create and configure an instance of the DataBaseBot.

    Args:
        debug (bool): Whether to run the bot in debug mode.
    """

    set_debug(debug)
    DEBUG = get_debug()

    # Set up logging
    logger = logging.getLogger(__name__)
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    intents = discord.Intents.default()
    intents.message_content = True
    bot = DataBaseBot(command_prefix=COMMAND_PREFIX, intents=intents)

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

        # Find the cogs dir
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cogs_path = os.path.join(dir_path, "cogs")
        # Load cogs
        for filename in os.listdir(cogs_path):
            if filename.endswith("_cog.py"):
                print(f"Loading cog: {filename}")
                cog_name = filename[:-3]
                try:
                    await bot.load_extension(f"app.cogs.{cog_name}")
                    logger.info(f"Loaded cog: {cog_name}")
                except Exception as e:
                    logger.error(f"Failed to load cog {cog_name}: {e}")

        # Unload the test cog outside of debug mode
        if not DEBUG:
            try:
                await bot.unload_extension("app.cogs.test_cog")
                logger.info("Unloaded test_cog for production mode.")
            except Exception as e:
                logger.error(f"Failed to unload test_cog: {e}")

        logger.info(f"{bot.user.name} setup complete.")

    return bot


def run_prod():
    """Run the bot in production mode, without any debug features."""
    bot = _create_bot(debug=False)
    bot.run(DISCORD_TOKEN)


def run_dev():
    """Run the bot in development mode, with debug features enabled."""
    bot = _create_bot(debug=True)
    bot.run(DISCORD_TOKEN)


def main(argv=None):
    """Fallback method to run the bot with CLI args."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ApplicationTracker Bot")
    parser.add_argument(
        "--debug", action="store_true", help="Run the bot in debug mode"
    )
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
        return

    run_dev() if args.debug else run_prod()


if __name__ == "__main__":
    main()
