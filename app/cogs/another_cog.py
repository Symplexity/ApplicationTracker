import logging
from discord.ext import commands
from config import get_debug

DEBUG = get_debug()

logger = logging.getLogger(__name__)


class AnotherCog(commands.Cog):
    """A cog for additional bot commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="hello", help="Greets the user with a friendly message.")
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.send("Hello! How can I assist you today?")


async def setup(bot: commands.Bot) -> None:
    try:
        await bot.add_cog(AnotherCog(bot))
        print("AnotherCog loaded successfully.")
    except Exception as e:
        print(f"Failed to load AnotherCog: {e}")
        if DEBUG:
            logger.debug("Exception details:", exc_info=True)

    logger.info("Another cog loaded.")
