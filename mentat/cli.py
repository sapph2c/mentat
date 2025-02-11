from mentat.bot import NewBot
from mentat.config import get_token

import click
import rich
import logging

BANNER = """

 ███▄ ▄███▓▓█████  ███▄    █ ▄▄▄█████▓ ▄▄▄     ▄▄▄█████▓
▓██▒▀█▀ ██▒▓█   ▀  ██ ▀█   █ ▓  ██▒ ▓▒▒████▄   ▓  ██▒ ▓▒
▓██    ▓██░▒███   ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██  ▀█▄ ▒ ▓██░ ▒░
▒██    ▒██ ▒▓█  ▄ ▓██▒  ▐▌██▒░ ▓██▓ ░ ░██▄▄▄▄██░ ▓██▓ ░ 
▒██▒   ░██▒░▒████▒▒██░   ▓██░  ▒██▒ ░  ▓█   ▓██▒ ▒██▒ ░ 
░ ▒░   ░  ░░░ ▒░ ░░ ▒░   ▒ ▒   ▒ ░░    ▒▒   ▓▒█░ ▒ ░░   
░  ░      ░ ░ ░  ░░ ░░   ░ ▒░    ░      ▒   ▒▒ ░   ░    
░      ░      ░      ░   ░ ░   ░        ░   ▒    ░      
       ░      ░  ░         ░                ░  ░        
                                                        

Written with ❤️  by sapph2c
"""


@click.command()
@click.option("--config", help="Config file path", default="config.yml")
def cli(config: str):
    """ """
    logger = logging.getLogger(__name__)
    rich.print(BANNER)
    token = get_token(config)
    bot = NewBot()
    try:
        logger.info("starting up the discord bot")
        bot.run(token, log_handler=None)
    except Exception as e:
        logger.fatal(f"mentat crashed with exception: {e}")
