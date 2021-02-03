import utils
import feedparser

CONFIG = {}


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
            "title": entries[i]["title"],
            "url": entries[i]["link"].split("#")[0],
            "published": entries[i]["published"],
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
    # fetch_feed('https://github.com/dejavudwh.atom')
    feeds = fetch_feedlist()
    utils.format_json(feeds)