# Profile Updater

> 之前用Github官方提供的api实现了更新最新的Commit信息，后面为了实现通过全配置的RSS源来自动更新，就暂时放弃这部分了，后面可能会再去实现全配置其它的API

## 功能

- 实现全配置化的自动更新RSS内容到README指定位置
- TODO：支持其它的自定义API的数据内容

## 使用

```yaml
# user config
user:
  # 这部分是配置之后url会用到的参数 class是每个feed所属的标志
  params:
    # _class: github, id is the parameter that's going to be used in the URL
    github:
      id: dejavudwh
    zhihu:
      id: shadow-61-66

  # 声明feed
  # feedName: 和后面的feeds的键值相同
  # disable: 禁用
  # entryCount: 显示条目数
  feedList:
    # default feed
    - feedName: githubActivitiesFeed
      disable: False
      entryCount: 5
        
    - feedName: zhihuPostsFeed
      disable: False
      entryCount: 5

    # user feed
    - feedName: BlogFeed
      disable: True
      entryCount: 5


feeds:
  # default feed
  # three messages of the feed: title, url, date
  # url: rss源 参数用{}包裹，参数必须和user中的params相对应
  # params: url参数
  # style: 生成的样式，rss暂时只支持三个信息
  # tagStartName: readme中要插入的位置行 <!-- GITHUB:START -->
  githubActivitiesFeed:
    _class: github
    url: https://github.com/{id}.atom
    params: [id]
    style: '    - [{title}]({url}) - {date}'
    tagStartName: GITHUB:START
    tagEndName: GITHUB:END 

  zhihuPostsFeed:
    _class: zhihu
    url:  https://rsshub.app/zhihu/posts/people/{id}
    params: [id]
    style: '    - [{title}]({url}) - {date}'
    tagStartName: ZHIHUPOSTS:START
    tagEndName: ZHIHUPOSTS:END 

  # user feed
  BlogFeed: 
    _class:
    url: https://dejavudwh.cn/atom.xml
    params: []
    style: '- [{title}]({url}) - {date}'
    tagStartName: BLOGPOSTS:START
    tagEndName: BLOGPOSTS:END 

api:
  # default api
  - githubApi:
  - zhihuApi:
```