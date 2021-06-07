from bs4 import BeautifulSoup

from util import log


def find_chap_list(content: str, link_format="{}", format_map={}, list_class="listmain", ignore_chap=0):
    soup = BeautifulSoup(content, 'html.parser')
    tag_main_list = soup.find(class_=list_class)
    tag_chap_list = tag_main_list.find_all('a')

    ret = []
    for a in tag_chap_list[ignore_chap:]:
        link = a.get("href")
        if link is not None:
            format_map["chap_id"] = link
            title = ' '.join(a.string.split())
            ret.append((link_format.format(**format_map), title))
    log.log_info(ret)
    return ret


def parse_content(text: str, txt_class="showtxt") -> str:
    soup = BeautifulSoup(text, 'html.parser')
    tag_txt = soup.find(class_=txt_class)

    phase_list = []
    for s in tag_txt.stripped_strings:
        phase_list.append(s)

    return '\n\n'.join(phase_list[:-1])
