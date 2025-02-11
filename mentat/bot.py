import discord
import logging


class Bot(discord.Client):
    """
    Bot is the Discord client used by Mentat.
    """

    logger: logging.Logger = logging.getLogger(__name__)

    async def on_ready(self):
        self.logger.info("mentat has successfuly connected to discord")

    async def on_message(self, message):
        self.logger.info(f"[+] message from {message.author}: {message.content}")


def NewBot():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    return Bot(intents=intents)
