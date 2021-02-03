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
    global CONIFG
    CONFIG = utils.read_config()
    # fetch_feed('https://github.com/dejavudwh.atom')
    feeds = fetch_feedlist()
    # utils.format_json(feeds)
    # print(feeds)
    contentsMap = generate_readme(feeds)
    # print(contentsMap)
    update_readme(contentsMap)