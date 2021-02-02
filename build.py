import requests
import json
import utils


CONFIG = {}


class FetchGithub(object):
    def __init__(self):
        self.api = CONFIG.get('github-api')
        self.prefix = self.api['prefix']
        user = CONFIG.get('user')
        self.username = user.get('username')
        self.count = int(user.get('entry_count'))
        self.repos = utils.MyHeap(len=5)
        self.commits = {}

    def fetch_repos_name(self):
        url = self.prefix + self.api['repos'].replace('{user}', self.username)
        res = requests.get(url)
        data = json.loads(res.text)
        for i in range(len(data)):
            time = utils.githubtime_to_time(data[i]['pushed_at'])
            # print(data[i]['pushed_at'], time, data[i]['name'])
            utils.MyHeap.push(self.repos, (time, data[i]['name']))
            print(self.repos._data)

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
    fg.fetch_repos_name()
    # fg.fetch_commits()
    # print(utils.lt_time('2019-09-24T08:23:04Z', '2019-09-23T07:29:16Z'))