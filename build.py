import utils
import feedparser
import requests
import json
import urllib3


CONFIG = {}


# about rss start #
def fetch_feedlist():
    # Gets all feeds set by the user then fetch feed
    feedlist = CONFIG['user']['feedList']
    # feed formatting information 
    feeds = {}
    for feed in feedlist:
        if not feed['disable']:
            feeds[feed['feedName']] = fetch_feed(feed)

    return feeds


def fetch_feed(feed):
    url = get_feed_url(feed['feedName'])
    count = feed['entryCount']
    entries = feedparser.parse(url)["entries"]
    count = count if count < len(entries) else len(entries)
    return [
        {
            'title': entries[i]["title"],
            'url': entries[i]["link"].split("#")[0],
            'published': entries[i]["published"],
        }
        for i in range(count)
    ]
    

def get_feed_url(feedName):
    user = CONFIG['user']
    # get feed
    feeds = CONFIG['feeds']
    feed = feeds[feedName]
    # get url params
    _class = feed['_class']
    params = {}
    for param in feed['params']:
        params[param] = user['params'][_class][param]
        # print(params)
    # gen url
    url = feed['url']
    for key, value in params.items():
        url = url.replace('{' + key + '}', str(value))
    
    return url


def generate_readme(feeds):
    # Generates the string to be inserted 
    contentsMap = {}
    for key, value in feeds.items():
        template = CONFIG['feeds'][key]['style']
        contents = ''
        for v in value:
            s = template.replace('{title}', v['title']).replace('{url}', v['url']).replace('{date}', v['published'])
            contents += ('\n' + s)
        contentsMap[key] = contents
        
    return contentsMap


def find_tags(feedNames):
    # get all tags in readme
    tags = []
    for feedName in feedNames:
        feed = CONFIG['feeds'][feedName]
        tag = (feedName, feed['tagStartName'], feed['tagEndName'])
        tags.append(tag)
    
    return tags
# about rss end #


# about github api #
def fetch_repos_name(githubId):
    # TODO hard code
    url = CONFIG['api']['allGithubRepo']['url'].replace('{id}', githubId)
    res = requests.get(url, verify=False)
    data = json.loads(res.text)
    repos = utils.MyHeap()
    for i in range(len(data)):
        # time for compare
        time = utils.githubtime_to_time(data[i]['pushed_at'])
        utils.MyHeap.push(repos, (time, data[i]['name']))

    return repos


def fetch_commits():
    # TODO hard code
    githubId = CONFIG['user']['params']['github']['id']
    repos = fetch_repos_name(githubId)
    url = CONFIG['api']['allGithubCommit']['url'].replace('{owner}', githubId)
    count = CONFIG['user']['apiList'][0]['entryCount']

    for repo in repos.get_data():
        res = requests.get(url.replace('{repo}', repo[1]), verify=False)
        data = json.loads(res.text)
        count = count if count < len(data) else len(data)
        commits = utils.MyHeap()
        for i in range(count):
            commit = data[i]['commit']
            date = commit['committer']['date']
            time = utils.githubtime_to_time(date)
            utils.MyHeap.push(commits, (time, (commit['message'], data[i]['html_url'], repo[1], date)))
    
    return commits
# about github api end #


# about update readme #
def update_readme(contentsMap):
    feedNames = []
    for key in contentsMap:
        feedNames.append(key)
    tags = find_tags(feedNames)
    posMap = {}
    rows = 0
    lines = []
    # location within the tag that needs to be updated
    needUpdate = False
    with open('README.md', 'r', encoding='UTF-8') as f:
        # Read the file and skip the locations that need to be updated
        for line in f:
            if not needUpdate:
                lines.append(line)
                rows = rows + 1
            for tag in tags:
                if tag[1] in line:
                    posMap[tag[0]] = rows
                    needUpdate = True
                elif tag[2] in line:
                    rows = rows + 1
                    lines.append(line)
                    needUpdate = False
    # insert
    i = 0
    for key, value in contentsMap.items():
        pos = posMap[key]
        # print(key, value)
        lines.insert(pos + i, value + '\n')    
        i = i + 1  
    
    content = ''.join(lines)
    file = open('README.md', 'w', encoding='UTF-8')
    file.write(content)
    file.close()


if __name__ == '__main__':
    urllib3.disable_warnings()
    global CONIFG
    CONFIG = utils.read_config()
    # fetch_feed('https://github.com/dejavudwh.atom')
    # feeds = fetch_feedlist()
    # utils.format_json(feeds)
    # print(feeds)
    # contentsMap = generate_readme(feeds)
    # print(contentsMap)
    # utils.format_json(CONFIG)
    commits = fetch_commits()
    utils.format_json(commits)
    # update_readme(contentsMap)