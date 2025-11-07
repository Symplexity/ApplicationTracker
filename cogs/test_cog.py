"""
A cog module for testing purposes. Contains some simple test commands.
"""

import logging
from discord.ext import commands
from config import DEBUG


logger = logging.getLogger(__name__)


class Test(commands.Cog):
    """A cog for testing bot commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(
        name="ping", help="Responds with 'Pong!' to test bot responsiveness."
    )
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("Pong!")

    @commands.command("test_debug", help="Checks if the bot is in debug mode.")
    async def test_debug(self, ctx: commands.Context) -> None:
        if DEBUG:
            await ctx.send("The bot is running in DEBUG mode.")
        else:
            await ctx.send("The bot is running in PRODUCTION mode.")


async def setup(bot: commands.Bot) -> None:
    """Setup function to add the Test cog to the bot."""
    try:
        await bot.add_cog(Test(bot))
    except Exception as e:
        logger.error(f"Failed to load Test cog: {e}")
        if DEBUG:
            logger.debug("Exception details:", exc_info=True)

    logger.info("Test cog loaded.")
