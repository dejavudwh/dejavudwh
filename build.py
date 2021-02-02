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
        config[section] = {}
        items = cp.items(section)
        for item in items:
            config[section][item[0]] = item[1]

    return config


class FetchGithub(object):
    def __init__(self):
        self.api = CONFIG.get('github-api')
        self.username = CONFIG.get('user').get('username')

    def fetch_repos_name(self):
        url = self.api['prefix'] + self.api['repos'].replace('{user}', self.username)
        res = requests.get(url)
        data = json.loads(res.text)
        format_json(len(data))

    def fetch_commits(self):
        pass


def format_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))


if __name__ == '__main__':
    global CONIFG
    CONFIG = read_config()
    # print(CONFIG)
    fg = FetchGithub()
    fg.fetch_repos_name()