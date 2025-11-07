"""
This cog handles the main commands for application tracking functionality.
"""

import logging
from discord.ext import commands
from config import get_debug

DEBUG = get_debug()

logger = logging.getLogger(__name__)


# TODO: Replace with actual database
# Temporary in-memory storage for tracked applications.
class Application:
    def __init__(self, name: str, status: str = "Applied"):
        self.name = name
        self.status = status


applications: dict[str, Application] = {}


class TrackerCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="track", help="Track a new application.")
    async def track(self, ctx: commands.Context, application_name: str) -> None:
        if application_name in applications:
            await ctx.send(
                f"Application '{application_name}' is already being tracked."
            )
        else:
            applications[application_name] = Application(name=application_name)
            await ctx.send(f"Started tracking application '{application_name}'.")


async def setup(bot: commands.Bot) -> None:
    try:
        await bot.add_cog(TrackerCog(bot))
        print("TrackerCog loaded successfully.")
    except Exception as e:
        print(f"Failed to load TrackerCog: {e}")
        if DEBUG:
            logger.debug("Exception details:", exc_info=True)

    logger.info("Tracker cog loaded.")
