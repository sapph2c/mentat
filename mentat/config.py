import yaml


def get_token(config: str) -> str:
    with open(config) as f:
        return yaml.load(f, Loader=yaml.FullLoader)["TOKEN"]
