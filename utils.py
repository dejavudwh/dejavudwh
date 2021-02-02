# -*- coding: utf-8 -*-

import json
from configparser import ConfigParser
import os
import datetime
import heapq
import time


def format_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))


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
    # print(config)
    return config


def githubtime_to_time(g_time):
    dt = datetime.datetime.strptime(g_time, "%Y-%m-%dT%H:%M:%SZ")
    return time.mktime(dt.timetuple())


def lt_time(time1, time2):
    time1 = githubtime_to_time(time1)
    time2 = githubtime_to_time(time2)

    return time1 - time2


class MyHeap(object):
    def __init__(self, initial=None, key=lambda x : x, len=100):
        self.k = len      
        self.key = key
        self._data = []

    def push(self, item):
        if len(self._data) < self.k:
            heapq.heappush(self._data, (self.key(item[0]), item[1]))
        else:
            topk_small = list(self._data[0])
            if item[0] > topk_small[0]:  
                heapq.heapreplace(self._data, (self.key(item[0]), item[1]))

    def pop(self):
        if(len(self._data) > 1):
            return heapq.heappop(self._data)[1]
        else:
            return None

    def get_data(self):
        return self._data