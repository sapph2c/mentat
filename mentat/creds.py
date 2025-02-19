from discord.ext import tasks, commands

import logging
import re
import yaml
import paramiko


class Credentials:
    """
    Credentials contains the data for a set of creds.
    """

    def __init__(self, pass_type: str, username: str, password: str):
        self.pass_type: str = pass_type
        self.username: str = username
        self.password: str = password

    def __repr__(self) -> str:
        return f"type: {self.pass_type}, username: {self.username}, password: {self.password}"

    def __eq__(self, other) -> bool:
        return (
            self.pass_type == other.pass_type
            and self.username == other.username
            and self.password == other.password
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

    def remove_creds(self, creds: Credentials):
        """
        remove_creds removes creds from the host.
        """
        self.credentials.remove(creds)

    async def update_creds(self):
        """
        update_creds pushes all credential changes to the host channel in Discord.
        """
        # build the message
        msg = "Current working credentials:\n"
        if self.credentials:
            for creds in self.credentials:
                msg += f"- **{creds.pass_type.upper()}**: `{creds.username}`:`{creds.password}`\n"
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
        return self.channel.name.replace("_", ".")


class CredManagement(commands.Cog):
    """
    CreManagement contains the set of commands used for credential management.
    """

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.hosts: list[Host] = []
        self.updatecreds.start()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @tasks.loop(seconds=5.0)
    async def updatecreds(self):
        """
        updatecreds is a background task that updates all known credentials for each host in Discord.
        """
        self.logger.info("updating creds")
        for host in self.hosts:
            self.checkcreds(host)
            await host.update_creds()

    def checkcreds(self, host: Host):
        """
        checkcreds validates that all host credentials are working.
        """
        self.logger.info("checking creds")
        for cred in host.credentials:
            if not self.cred_is_working(host.get_ip(), cred):
                host.remove_creds(cred)

    def cred_is_working(self, ip: str, cred: Credentials) -> bool:
        """
        cred_is_working validates credentials by invoking each credential types specific checker.
        """
        match cred.pass_type:
            case "ssh":
                return self.check_ssh(ip, cred)
            case _:
                return False

    def check_ssh(self, ip: str, cred: Credentials) -> bool:
        """
        check_ssh attempts an SSH connection using the specified credentials against the target, and returns True if the attempt is successful.
        """
        try:
            self.ssh.connect(
                ip, port=22, username=cred.username, password=cred.password
            )
            return True
        except Exception as e:
            self.logger.error(e)
            return False

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
            self.hosts = []
        except Exception as e:
            self.logger.error(e)

    @commands.command()
    async def addcreds(
        self, ctx, ip: str, pass_type: str, username: str, password: str
    ):
        """
        Add creds to a host, positional arguments are <ip> <pass_type> <username> <password
        """
        try:
            for host in self.hosts:
                if ip == host.get_ip():
                    new_creds = Credentials(pass_type, username, password)
                    self.logger.info(f"{ip}: adding creds: {new_creds}")
                    host.add_creds(new_creds)
        except Exception as e:
            self.logger.error(e)

    @commands.command()
    async def addhosts(self, ctx):
        """
        Adds hosts to mentat via `.yaml` file
        """
        try:
            for attachment in ctx.message.attachments:
                self.logger.info(f"adding hosts from: {attachment.filename}")
                content = await attachment.read()
                hostlist = yaml.safe_load(content)
                for ip_addr, data in hostlist.items():
                    # sanitize for Discord channel name conventions
                    santitized_ip = ip_addr.replace(".", "_")
                    if santitized_ip in self.hosts:
                        continue

                    channel = await ctx.guild.create_text_channel(santitized_ip)
                    new_host = Host(channel)
                    # add all host creds
                    if data:
                        for pass_type, creds_block in data["creds"].items():
                            for username, password in creds_block.items():
                                new_creds = Credentials(pass_type, username, password)
                                new_host.add_creds(new_creds)
                    self.hosts.append(new_host)
        except Exception as e:
            self.logger.error(e)
