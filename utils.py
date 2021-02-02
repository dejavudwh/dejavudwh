import json
from configparser import ConfigParser
import os


def format_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))


def read_config():
    cp = ConfigParser()
    config = {}

    file_path = os.path.join(os.path.abspath('.'), 'config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError("配置文件不存在")

    cp.read(file_path)

    sections = cp.sections()
    for section in sections:
        config[section] = {}
        items = cp.items(section)
        for item in items:
            config[section][item[0]] = item[1]

    return config