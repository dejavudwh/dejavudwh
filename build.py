import requests
import json
import utils


CONFIG = {}


class FetchGithub(object):
    def __init__(self):
        self.api = CONFIG.get('github-api')
        self.username = CONFIG.get('user').get('username')

    def fetch_repos_name(self):
        url = self.api['prefix'] + self.api['repos'].replace('{user}', self.username)
        res = requests.get(url)
        data = json.loads(res.text)
        utils.format_json(len(data))

    def fetch_commits(self):
        pass


if __name__ == '__main__':
    global CONIFG
    CONFIG = utils.read_config()
    # print(CONFIG)
    fg = FetchGithub()
    fg.fetch_repos_name()