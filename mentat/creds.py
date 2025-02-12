from discord.ext import tasks, commands

import logging
import re
import yaml


class CredManagement(commands.Cog):
    """
    CreManagement contains the set of commands used for credential management.
    """

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.hosts: list[Host] = []
        self.updatecreds.start()

    @commands.command()
    async def addcreds(self, ctx, ip: str, username: str, password: str):
        """
        Add creds to a host
        """
        try:
            for host in self.hosts:
                host_ip = host.get_ip()
                if host_ip == ip.replace(".", "_"):
                    new_creds = Credentials(username, password)
                    self.logger.info(f"{host_ip}: adding creds: {new_creds}")
                    host.add_creds(new_creds)
        except Exception as e:
            self.logger.error(e)

    @commands.command()
    async def addhosts(self, ctx):
        """
        Adds hosts to mentat via a newline separated list
        """
        try:
            for attachment in ctx.message.attachments:
                self.logger.info(f"adding hosts from: {attachment.filename}")
                content = await attachment.read()
                hostlist = yaml.safe_load(content)
                for ip, data in hostlist.items():
                    # sanitize for Discord channel name conventions
                    ip = ip.replace(".", "_")
                    if ip not in self.hosts:
                        channel = await ctx.guild.create_text_channel(ip)
                        new_host = Host(channel)
                        # add all host creds
                        if data:
                            for username, password in data["creds"].items():
                                self.logger.info(username)
                                self.logger.info(password)
                                new_creds = Credentials(username, password)
                                new_host.add_creds(new_creds)
                        self.hosts.append(new_host)
        except Exception as e:
            self.logger.error(e)

    @tasks.loop(seconds=5.0)
    async def updatecreds(self):
        """
        updatecreds is a background task that updates all known credentials for each host in Discord.
        """
        self.logger.info("updating creds")
        for host in self.hosts:
            await host.update_creds()

    @commands.command()
    async def purge(self, ctx):
        """
        purge removes all previous host channels. Use on mentat startup
        """
        self.logger.info("purging channels")
        try:
            for channel in self.bot.get_all_channels():
                if re.match(r"^[0-9]+_[0-9]+_[0-9]+_[0-9]+$", channel.name):
                    await channel.delete()
        except Exception as e:
            self.logger.error(e)


class Credentials:
    """
    Credentials contains the data for a set of creds.
    """

    def __init__(self, username: str, password: str, type: str):
        self.username: str = username
        self.password: str = password
        self.type: str = type

    def __repr__(self) -> str:
        return f"{type}: username: {self.username}, password: {self.password}"

    def __eq__(self, other) -> bool:
        return (
            self.username == other.username
            and self.password == other.password
            and self.type == other.type
        )


class Host:
    """
    Host contains the data for a target host.
    """

    def __init__(self, channel):
        self.channel = channel
        self.credentials: list[Credentials] = []
        self.creds_msg = None

    def add_creds(self, creds: Credentials):
        """
        add_creds adds creds to the host.
        """
        self.credentials.append(creds)

    async def update_creds(self):
        """
        update_creds pushes all credential changes to the host channel in Discord.
        """
        # build the message
        msg = "Current working credentials:\n"
        if self.credentials:
            for creds in self.credentials:
                msg += f"- `{creds.username}`: `{creds.password}`\n"
        else:
            msg += "none :("

        # create the pinned cred msg if it doesn't exist
        if not self.creds_msg:
            self.creds_msg = await self.channel.send(msg)
            await self.creds_msg.pin()
        # otherwise update the pinned msg
        else:
            await self.creds_msg.edit(content=msg)

    def get_ip(self) -> str:
        return self.channel.name
