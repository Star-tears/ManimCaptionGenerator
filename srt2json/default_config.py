import json


def get_config():
    with open("default_config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        return config
