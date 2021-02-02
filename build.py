from configparser import ConfigParser
import os
import requests
import json


CONFIG = {}


def read_config():
    cp = ConfigParser()
    config = {}

    file_path = os.path.join(os.path.abspath('.'), 'config.ini')
    if not os.path.exists(file_path):
        raise FileNotFoundError("配置文件不存在")

    cp.read(file_path)

    sections = cp.sections()
    for section in sections:
        items = cp.items(section)
        for item in items:
            config[item[0]] = item[1]

    print(config)
    

def format_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))


if __name__ == '__main__':
    read_config()