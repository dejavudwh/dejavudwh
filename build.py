import requests
import json
import utils
import string


CONFIG = {}


class FetchGithub(object):
    def __init__(self):
        self.api = CONFIG.get('github-api')
        self.prefix = self.api['prefix']
        user = CONFIG.get('user')
        self.username = user.get('username')
        self.count = int(user.get('entry_count'))
        self.repos = utils.MyHeap(len=self.count)
        self.commits = utils.MyHeap(len=self.count)

    def fetch_repos_name(self):
        url = self.prefix + self.api['repos'].replace('{user}', self.username)
        res = requests.get(url)
        data = json.loads(res.text)
        for i in range(len(data)):
            time = utils.githubtime_to_time(data[i]['pushed_at'])
            utils.MyHeap.push(self.repos, (time, data[i]['name']))

    def fetch_commits(self):
        self.fetch_repos_name()
        url = self.prefix + self.api['commits'].replace('{owner}', self.username)
        for repo in self.repos.get_data():
            res = requests.get(url.replace('{repo}', repo[1]))
            data = json.loads(res.text)
            count = self.count if self.count < len(data) else len(data)
            for i in range(count):
                commit = data[i]['commit']
                date = commit['committer']['date']
                time = utils.githubtime_to_time(date)
                utils.MyHeap.push(self.commits, (time, (commit['message'], data[i]['html_url'], repo[1], date)))
        # utils.format_json(self.commits.get_data())


def generate_string(items):
    template = string.Template('    - [${message}](${url}) -repo: ${name} ${date}')
    s = ''
    for item in items:
        s += '\n'
        s += template.substitute(message=item[1][0], url=item[1][1], name=item[1][2], date=item[1][3])
        s += '\n'
    return s


def update_readme(template):
    lines = []
    rows = 0
    flag = False
    is_old = False
    with open('README.md', 'r', encoding='UTF-8') as f:
        for line in f:
            if not is_old:
                lines.append(line)
            if not flag:
                rows = rows + 1
            if 'COMMITS-LIST:START' in line:
                flag = True
                is_old = True
            elif 'COMMITS-LIST:END' in line:
                lines.append('\n' + line)
                is_old = False
    lines.insert(rows, template)      
    content = ''.join(lines)
    file = open('README.md', 'w', encoding='UTF-8')
    file.write(content)
    file.close()


if __name__ == '__main__':
    global CONIFG
    CONFIG = utils.read_config()
    # print(CONFIG)
    fg = FetchGithub()
    # fg.fetch_repos_name()
    fg.fetch_commits()
    new_readme = generate_string(fg.commits.get_data())
    update_readme(new_readme)