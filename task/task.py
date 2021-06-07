from typing import List
import time

import requests
from requests.models import HTTPError
from sqlitedict import SqliteDict

from option import Option
from util import log
from util import parser

global_task_cache = SqliteDict('./temp.sqlite', autocommit=True)


class Task:

    def __init__(self, id: int, chap_list: List[any], opt: Option):
        super().__init__()
        self.id = id
        self.chap_list = chap_list
        self.opt = opt
        self.content_list = []
        self.completed = False

    def run(self):
        n = len(self.chap_list)
        i = 1
        for link, title in self.chap_list:
            chap_content = self.fetch_cache(title)
            if chap_content is None:
                chap_content = title + '\n\n' + self.http_get(link, retry=1)
                self.save_cache(title, chap_content)
            self.content_list.append(chap_content)
            log.log_info("Task#{}: {}/{}".format(self.id, i, n))
            i += 1
        self.completed = True

    def fetch_cache(self, title: str):
        return global_task_cache.get(title, None)

    def save_cache(self, title: str, content: str):
        global_task_cache[title] = content

    def loads(self) -> str:
        if not self.completed:
            return "Task not completed"
        return '\n'.join(self.content_list)

    def http_get(self, url, retry=1) -> str:
        r = requests.get(url)
        if r.status_code != 200:
            log.log_error("request failed: {}".format(r.status_code))
            if retry > 0:
                time.sleep(2)
                return self.http_get(url, retry-1)
            raise HTTPError(request=r.request, response=r)
        html_text = r.content.decode('utf-8')
        chap_content = parser.parse_content(
            html_text, self.opt.chap_content_class)
        return chap_content


def close_cache():
    global_task_cache.close()


def clear_cache():
    global_task_cache.clear()
