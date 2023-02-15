import os
import json

with open("module/config.json", "r") as f:
    config = json.load(f)


def get_config(config_name):
    return config[config_name]
