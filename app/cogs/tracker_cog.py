"""
This cog handles the main commands for application tracking functionality.
"""

import logging
from discord.ext import commands
from app.config import get_debug

DEBUG = get_debug()

logger = logging.getLogger(__name__)


class TrackerCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="track", help="Track a new application.")
    async def track(self, ctx: commands.Context, application_name: str) -> None:
        # Fetch all tracked applications from the "database"
        cur = self.bot.conn.cursor()
        cur.execute("SELECT name FROM tracked_applications")
        tracked_apps = [row[0] for row in cur.fetchall()]
        cur.close()
        if application_name in tracked_apps:
            await ctx.send(
                f"Application '{application_name}' is already being tracked."
            )
        else:
            cur = self.bot.conn.cursor()
            cur.execute(
                "INSERT INTO tracked_applications (name, status) VALUES (%s, %s)",
                (application_name, "Applied"),
            )
            self.bot.conn.commit()
            cur.close()
            await ctx.send(f"Started tracking application '{application_name}'.")

    @commands.command(
        name="all_applications", aliases=["all"], help="List all tracked applications."
    )
    async def all_applications(self, ctx: commands.Context) -> None:
        # Fetch all tracked applications from the "database"
        cur = self.bot.conn.cursor()
        cur.execute("SELECT name, status FROM tracked_applications")
        rows = cur.fetchall()
        cur.close()
        if not rows:
            await ctx.send("No applications are currently being tracked.")
            return

        # TODO: Improve formatting of the output, possibly using embeds.
        response = "Tracked Applications:\n"
        for name, status in rows:
            response += f"- {name}: {status}\n"
        await ctx.send(response)


async def setup(bot: commands.Bot) -> None:
    try:
        await bot.add_cog(TrackerCog(bot))
        print("TrackerCog loaded successfully.")
    except Exception as e:
        print(f"Failed to load TrackerCog: {e}")
        if DEBUG:
            logger.debug("Exception details:", exc_info=True)

    logger.info("Tracker cog loaded.")
