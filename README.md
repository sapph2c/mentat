# Mentat

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fsapph2c%2Fmentat%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python&logoSize=auto)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sapph2c/mentat/ci.yml?style=for-the-badge&logo=github&logoSize=auto)
![GitHub deployments](https://img.shields.io/github/deployments/sapph2c/mentat/pypi?style=for-the-badge&logo=pypi&logoColor=white&logoSize=auto)

Discord bot designed to streamline credential management and access tracking during red team engagements.

## Usage

Mentat is managed using Discord `/` commands.

Management commands include:

- `/purge`: Removes all previous host channels
- `/addhosts`: Adds a list of hosts from an attached newline separated file.
- `/addcreds <host ip> <username> <password>`: Adds new credentials to a specified host.

## File formats

Example `hostlist.txt` file:

```
192.168.56.1:
  creds:
    test_user: test_pass
    hello: world

192.168.56.2
192.168.56.3
```
