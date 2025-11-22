"""
A utility to check if a bot is a DB bot, and that the connection is valid.
"""

from app.bot import DataBaseBot


def check_bot(bot) -> bool:
    """
    Check if the provided bot is an instance of DataBaseBot and has a valid connection.

    Args:
        bot: The bot instance to check.

    Returns:
        bool: True if the bot is a DataBaseBot with a valid connection, False otherwise.
    """
    if not isinstance(bot, DataBaseBot):
        return False
    if not hasattr(bot, "conn") or bot.conn is None:
        return False
    return True
