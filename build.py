import requests
import json
import utils
import datetime


CONFIG = {}


class FetchGithub(object):
    def __init__(self):
        self.api = CONFIG.get('github-api')
        self.prefix = self.api['prefix']
        user = CONFIG.get('user')
        self.username = user.get('username')
        self.count = int(user.get('entry_count'))
        self.repos = []
        self.commits = {}

    def fetch_repos_name(self):
        url = self.prefix + self.api['repos'].replace('{user}', self.username)
        res = requests.get(url)
        data = json.loads(res.text)
        for i in range(2):
            self.repos.append(data[i]['name'])

    def fetch_commits(self):
        self.fetch_repos_name()
        url = self.prefix + self.api['commits'].replace('{owner}', self.username)
        for repo in self.repos:
            res = requests.get(url.replace('{repo}', repo))
            data = json.loads(res.text)
            # utils.format_json(data[1]['commit'])
            commit = []
            for i in range(self.count):
                commit.append(data[i]['commit'])
            self.commits[repo] = commit


if __name__ == '__main__':
    global CONIFG
    CONFIG = utils.read_config()
    # print(CONFIG)
    fg = FetchGithub()
    fg.fetch_commits()
    # print(datetime.datetime(2021, 4, 1, 12,32,12).__gt__(datetime.datetime(2021, 4, 1, 12,22,12)))