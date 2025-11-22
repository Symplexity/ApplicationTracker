"""
This cog handles the main commands for application tracking functionality.
"""

import logging
from discord.ext import commands
from app.config import get_debug, TABLE_NAME, TABLE_LAYOUT

DEBUG = get_debug()

logger = logging.getLogger(__name__)


class TrackerCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="track", help="Track a new application.")
    async def track(self, ctx: commands.Context, application_name: str) -> None:
        try:
            # Fetch all tracked applications from the "database"
            cur = self.bot.conn.cursor()
            cur.execute(f"SELECT name FROM {TABLE_NAME}")
            tracked_apps = [row[0] for row in cur.fetchall()]
            cur.close()
            if application_name in tracked_apps:
                await ctx.send(
                    f"Application '{application_name}' is already being tracked."
                )
            else:
                cur = self.bot.conn.cursor()
                cur.execute(
                    f"INSERT INTO {TABLE_NAME} (name, status) VALUES (%s, %s)",
                    (application_name, "Applied"),
                )
                self.bot.conn.commit()
                cur.close()
                await ctx.send(f"Started tracking application '{application_name}'.")
        except Exception as e:
            self.bot.conn.rollback()
            logger.error(f"Error tracking application: {e}")
            if DEBUG:
                logger.debug("Exception details:", exc_info=True)
            await ctx.send("An error occurred while trying to track the application.")

    @commands.command(
        name="all_applications", aliases=["all"], help="List all tracked applications."
    )
    async def all_applications(self, ctx: commands.Context) -> None:
        try:
            # Fetch all tracked applications from the "database"
            cur = self.bot.conn.cursor()
            cur.execute(f"SELECT name, status, applied_date FROM {TABLE_NAME}")
            rows = cur.fetchall()
            cur.close()
            if not rows:
                await ctx.send("No applications are currently being tracked.")
                return

            # TODO: Improve formatting of the output, possibly using embeds.
            response = "Tracked Applications:\n"
            for name, status, applied_date in rows:
                response += f"- {name}: {status} (Applied on: {applied_date})\n"
            await ctx.send(response)
        except Exception as e:
            self.bot.conn.rollback()
            logger.error(f"Error fetching applications: {e}")
            if DEBUG:
                logger.debug("Exception details:", exc_info=True)
            await ctx.send("An error occurred while fetching tracked applications.")

    @commands.command(
        name="reset_table",
        aliases=["reset"],
        help="Reset the tracked applications table. Warning: This will delete all data.",
    )
    async def reset_table(self, ctx: commands.Context) -> None:
        # Ask user for confirmation
        await ctx.send(
            "Are you sure you want to reset the tracked applications table? This will delete all data. Respond to this message with 'yes' to confirm."
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30.0)
            if msg.content.lower() == "yes":
                cur = self.bot.conn.cursor()
                cur.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
                cur.execute(f"CREATE TABLE {TABLE_NAME} {TABLE_LAYOUT}")
                self.bot.conn.commit()
                cur.close()
                await ctx.send("Tracked applications table has been reset.")
            else:
                await ctx.send("Table reset cancelled.")
        except TimeoutError as e:
            await ctx.send("No confirmation received. Table reset cancelled.")
            if DEBUG:
                logger.debug(f"({e}) Exception details: ", exc_info=True)
        except Exception as e:
            self.bot.conn.rollback()
            logger.error(f"Error resetting table: {e}")
            if DEBUG:
                logger.debug("Exception details:", exc_info=True)
            await ctx.send("An error occurred while resetting the table.")


async def setup(bot: commands.Bot) -> None:
    try:
        await bot.add_cog(TrackerCog(bot))
        print("TrackerCog loaded successfully.")
    except Exception as e:
        print(f"Failed to load TrackerCog: {e}")
        if DEBUG:
            logger.debug("Exception details:", exc_info=True)

    logger.info("Tracker cog loaded.")
