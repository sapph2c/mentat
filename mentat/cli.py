from mentat.creds import CredManagement
from mentat.config import get_token
from discord.ext import commands
from discord import Intents
from rich.logging import RichHandler
from pythonjsonlogger.json import JsonFormatter


import asyncclick as click
import logging

# set logging configuration
discord_logger = logging.getLogger("discord")
handler = RichHandler()
handler.setFormatter(JsonFormatter())
discord_logger.addHandler(handler)
discord_logger.setLevel(logging.INFO)


@click.command()
@click.option("--config", help="Config file path", default="config.yml")
async def cli(config: str):
    """
    Mentat Discord bot CLI.
    """
    # fetch the token from config.yml
    token = get_token(config)
    # create the Discord bot
    bot = commands.Bot(command_prefix="/", intents=Intents.all())
    # register the credentials management commands
    await bot.add_cog(CredManagement(bot))
    try:
        # start Mentat
        discord_logger.info("starting up the discord bot")
        await bot.start(token)
    except Exception as e:
        # log and catch any exceptions
        discord_logger.fatal(f"mentat crashed with exception: {e}")
