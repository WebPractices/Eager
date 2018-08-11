# coding=utf-8
from datetime import datetime

from lxml import etree
from app.utils.parse_url import parse_url


class ParseCrawler(object):
    """
    source: {'biquge': 'http://www.biquge.com.tw/'}
    """
    def __init__(self):
        self._biquge_base_url = 'http://www.biquge.com.tw'
        self.novel_state = {}
        self._state_xpath = '//*[@id="info"]/p[3]/text()'

    def _novel_state(self, name, update_info):
        """get novels state, judge this novel is finished or unfinished"""
        spt = list(map(int, update_info[5:].split('-')))
        update_time = datetime(spt[0], spt[1], spt[2])
        crawl_time = datetime.now()
        interval_days = (crawl_time - update_time).days
        self.novel_state[name] = '更新中' if interval_days < 7 else '完结'

    def get_menu(self, name, novel_url):
        """crawling the novel catalog page"""
        res = parse_url(novel_url, 'gbk')
        html = etree.HTML(res)

        # get update time
        update_info = html.xpath(self._state_xpath)[0]
        self._novel_state(name, update_info)

        chapter_url = html.xpath('//*[@id="list"]/dl/dd/a/@href')
        chapter_title = html.xpath('//*[@id="list"]/dl/dd/a/text()')
        for url, title in zip(chapter_url, chapter_title):
            chapter = {
                'url': self._biquge_base_url + url,
                'title': title
            }
            yield chapter

    def get_chapter(self, chapter_url):
        """crawler chapter content"""
        res = parse_url(chapter_url, 'gbk')
        html = etree.HTML(res)
        content = html.xpath('//*[@id="content"]/text()')
        return ''.join(content)

    def __call__(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    crawler = CrawlBiquge()
