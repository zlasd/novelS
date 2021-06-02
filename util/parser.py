from bs4 import BeautifulSoup

from util import log

def find_chap_list(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    tag_main_list = soup.find(class_="listmain")
    tag_chap_list = tag_main_list.find_all('a')

    ret = {}
    for a in tag_chap_list[:5]:
        log.log_info(a.get("href"), a.string)
        link = a.get("href")
        if link is not None:
            ret[link] = a.string
    return ret