import requests
from requests.exceptions import RequestException
from requests.models import HTTPError

import task
from option import Option
from task import Task
from util import log
from util import parser

# pylint: disable=no-member


class TaskManager:
    def __init__(self, opt_name: str, book_id: str):
        super().__init__()
        self.opt = Option(opt_name)
        self.book_id = book_id

    def run(self, retry=3):
        try:
            self.prepare()
            self.split_task()
            self.collect_result()
            self.sweep()
        except RequestException as e:
            log.log_error("HTTP error", e)
            log.log_info("task failed")
            task.close_cache()
            if retry > 0:
                time.sleep(5)
                self.run(retry-1)
            raise e

    def prepare(self):
        # http get main page
        # parse chapter list
        format_map = {"book_id": self.book_id}
        book_url = self.opt.book_page_format.format(**format_map)
        r = requests.get(book_url)
        if r.status_code != 200:
            log.log_error("request failed: {}".format(r.status_code))
            raise HTTPError(request=r.request, response=r)
        html_text = r.content.decode('utf-8')

        self.chap_list = parser.find_chap_list(html_text, link_format=self.opt.chap_page_format,
                                               format_map=format_map, list_class=self.opt.chap_list_class, ignore_chap=self.opt.ignore_chap)

    def split_task(self):
        # split chapter url to task
        batch_num = self.opt.get_batch_num()
        i = 0
        task_list = []
        while i*batch_num < len(self.chap_list):
            chap_batch = self.chap_list[i*batch_num:(i+1)*batch_num]
            task_list.append(Task(i, chap_batch, self.opt))
            i += 1

        i = 1
        self.task_list = task_list
        for t in self.task_list:
            t.run()
            log.log_info("Task#{} done!".format(i))
            i += 1

    def collect_result(self):
        # collect result to full txt
        task_result = []
        for t in self.task_list:
            task_result.append(t.loads())
        self.result = '\n'.join(task_result)
        self.save()

    def save(self):
        log.write(self.result, "{}.txt".format(self.book_id))

    def sweep(self):
        task.clear_cache()
