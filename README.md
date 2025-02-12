# Mentat

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fsapph2c%2Fmentat%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python&logoSize=auto)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sapph2c/mentat/ci.yml?style=for-the-badge&logo=github&logoSize=auto)
![GitHub deployments](https://img.shields.io/github/deployments/sapph2c/mentat/pypi?style=for-the-badge&logo=pypi&logoColor=white&logoSize=auto)

Discord bot designed to streamline credential management and access tracking during red team engagements.

## Installation

Mentat is available as a Python package on PyPI and can be installed using `uv` (recommended), `pipx`, or `pip`.

**Note**: python 3.12 is required (currently does not support python 3.13)

It's recommended that you create a virtual environment before installation:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install using uv:

```bash
uv tool install mentat-bot@latest
```

Install using pipx:

```bash
pipx install mentat-bot
```

Install using pip:

```bash
pip install mentat-bot
```

## Usage

In order to use Mentat, a bot account must first be created on Discord and invited to the server you want to use for your engagement. This can be done by following the guide at: https://discordpy.readthedocs.io/en/stable/discord.html

After installing, invoke the bot by simply running:

```bash
mentat
```

The Discord bot token should be available within your current directory in a file called `config.yml` or specified via `--path` when invoking the Mentat CLI.

## Features

- Automatic credential tracking for `SSH`
- Red Team ChatOps via Discord `/` commands.

## Commands

Mentat is managed using Discord `/` commands.

Management commands include:

- `/purge`: Removes all previous host channels
- `/addhosts`: Adds a list of hosts and credentials from an attached `.yaml` file
- `/addcreds <host ip> <type> <username> <password>`: Adds new credentials to a specified host

## File formats

Example `hosts.yaml` file:

```
192.168.56.1:
  creds:
    ssh:
      test_user: test_pass

192.168.56.2
192.168.56.3
```
