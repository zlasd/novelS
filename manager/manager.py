import requests

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

    def run(self):
        self.prepare()
        self.split_task()

    def prepare(self):
        # http get main page
        # parse chapter list
        book_url = self.opt.book_page_format.format(self.book_id)
        r = requests.get(book_url)
        if r.status_code != 200:
            log.log_error("request failed: {}".format(r.status_code))
        html_text = r.content.decode('utf-8')
        log.write(html_text)

        self.chap_list = parser.find_chap_list(html_text)

    def split_task(self):
        # split chapter url to task
        pass

    def collect_result(self):
        # collect result to full txt
        pass
