"""
A cog module for testing purposes. Contains some simple test commands.
"""

import logging
from discord.ext import commands
from config import get_debug

DEBUG = get_debug()

logger = logging.getLogger(__name__)


def move_to_root(func):
    async def wrapper(*args, **kwargs):
        import os

        original_path = os.getcwd()
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logger.debug(f"Changed working directory to {os.getcwd()} for {func.__name__}.")
        result = await func(*args, **kwargs)
        os.chdir(original_path)
        logger.debug(
            f"Restored working directory to {os.getcwd()} after {func.__name__}."
        )
        return result

    return wrapper


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

    @commands.command(
        "list_cogs",
        aliases=["lc", "cogs", "list"],
        help="Lists all currently loaded cogs.",
    )
    async def list_cogs(self, ctx: commands.Context) -> None:
        cogs = list(self.bot.extensions.keys())
        if cogs:
            await ctx.send("Loaded cogs:\n" + "\n".join(cogs))
        else:
            await ctx.send("No cogs are currently loaded.")

    @commands.command(
        "unload_cog", aliases=["unload"], help="Unloads a specified cog by name."
    )
    async def unload_cog(
        self, ctx: commands.Context, cog_name: str | None = None
    ) -> None:
        if cog_name is None:
            await ctx.send("Please specify a cog name to unload.")
            return
        cog_full_name = f"cogs.{cog_name}"
        if cog_full_name in self.bot.extensions:
            try:
                await self.bot.unload_extension(cog_full_name)
                await ctx.send(f"Successfully unloaded cog: {cog_name}")
            except Exception as e:
                await ctx.send(f"Failed to unload cog {cog_name}: {e}")
                logger.debug("Exception details:", exc_info=True)
        else:
            await ctx.send(f"Cog {cog_name} is not loaded.")

    @commands.command(
        "load_cog", aliases=["load"], help="Loads a specified cog by name."
    )
    async def load_cog(
        self, ctx: commands.Context, cog_name: str | None = None
    ) -> None:
        if cog_name is None:
            await ctx.send("Please specify a cog name to load.")
            return
        cog_full_name = f"cogs.{cog_name}"
        if cog_full_name not in self.bot.extensions:
            try:
                await self.bot.load_extension(cog_full_name)
                await ctx.send(f"Successfully loaded cog: {cog_name}")
            except Exception as e:
                await ctx.send(f"Failed to load cog {cog_name}: {e}")
                logger.debug("Exception details:", exc_info=True)
        else:
            await ctx.send(f"Cog {cog_name} is already loaded.")

    @commands.command(
        "reload_cogs",
        aliases=["reload"],
        help="Reloads all cogs in the /cogs directory.",
    )
    @move_to_root
    async def reload_cogs(self, ctx: commands.Context) -> None:
        import os

        for filename in os.listdir("./cogs"):
            if filename.endswith("_cog.py"):
                cog_name = filename[:-3]  # Remove .py extension
                cog = f"cogs.{cog_name}"
                try:
                    if cog not in self.bot.extensions:
                        await self.bot.load_extension(cog)
                        await ctx.send(f"Loaded new cog: {cog_name}")
                    else:
                        await self.bot.reload_extension(cog)
                        await ctx.send(f"Reloaded cog: {cog_name}")
                except Exception as e:
                    await ctx.send(f"Failed to reload cog {cog_name}: {e}")
                    logger.debug("Exception details:", exc_info=True)


async def setup(bot: commands.Bot) -> None:
    """Setup function to add the Test cog to the bot."""
    try:
        await bot.add_cog(Test(bot))
    except Exception as e:
        logger.error(f"Failed to load Test cog: {e}")
        if DEBUG:
            logger.debug("Exception details:", exc_info=True)

    logger.info("Test cog loaded.")
