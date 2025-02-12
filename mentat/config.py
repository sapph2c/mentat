import yaml


def get_token(config: str) -> str:
    """
    get_token retrieves the Discord token from the provided `.yml` config file.
    """
    with open(config) as f:
        return yaml.load(f, Loader=yaml.FullLoader)["TOKEN"]
