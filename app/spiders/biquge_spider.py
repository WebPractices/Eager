# coding=utf-8
from datetime import datetime

from lxml import etree
from app.utils.parse_url import parse_url


class CrawlBiquge(object):
    """
    Biquge crawler
    source: http://www.biquge.com.tw/
    """
    def __init__(self):
        self._biquge = 'http://www.biquge.com.tw/{category}/'
        self._base_url = 'http://www.biquge.com.tw'
        self.novel = {}
        self._novel_html = None
        self._state_xpath = '//*[@id="info"]/p[3]/text()'
        self.novel['source'] = self._base_url

    def _novel_state(self, update_info):
        """get novels state, judge this novel is finished or unfinished"""
        spt = list(map(int, update_info[5:].split('-')))
        update_time = datetime(spt[0], spt[1], spt[2])
        crawl_time = datetime.now()
        interval_days = (crawl_time - update_time).days
        self.novel['state'] = '更新中' if interval_days < 7 else '完结'

    def get_url(self, category):
        """crawler all novels url according to category"""
        self.novel['category'] = category
        url = self._biquge.format(category=category)
        res = parse_url(url, 'gbk')
        html = etree.HTML(res)
        urls = html.xpath('//*[@id="newscontent"]/div[@class="l"]/ul/li/span[1]/a/@href')
        urls_r = html.xpath('//*[@id="newscontent"]/div[@class="r"]/ul/li/span[1]/a/@href')
        names = html.xpath('//*[@id="newscontent"]/div[@class="l"]/ul/li/span[1]/a/text()')
        names_r = html.xpath('//*[@id="newscontent"]/div[@class="r"]/ul/li/span[1]/a/text()')
        authors = html.xpath('//*[@id="newscontent"]/div[@class="l"]/ul/li/span[3]/text()')
        authors_r = html.xpath('//*[@id="newscontent"]/div[@class="r"]/ul/li/span[2]/text()')
        urls.extend(urls_r)
        names.extend(names_r)
        authors.extend(authors_r)
        for url, name, author in zip(urls, names, authors):
            novel = {
                'url': url,
                'name': name,
                'author': author
            }
            yield novel

    def get_info(self, name, novel_url):
        """crawler novel info"""
        res = parse_url(novel_url, 'gbk')
        html = etree.HTML(res)
        self._novel_html = html
        image = html.xpath('//*[@id="fmimg"]/img/@src')
        intro = html.xpath('//*[@id="intro"]/p/text()')
        self.novel['image'] = image
        self.novel['intro'] = intro
        # get update time
        update_info = html.xpath(self._state_xpath)[0]
        self._novel_state(update_info)
        return self.novel

    def get_menu(self, name=None, url=None):
        """crawling novel menu"""
        if not self._novel_html:
            if name and url:
                self.get_info(name, url)
            else:
                return False
        chapter_url = self._novel_html.xpath('//*[@id="list"]/dl/dd/a/@href')
        chapter_title = self._novel_html.xpath('//*[@id="list"]/dl/dd/a/text()')
        for url, title in zip(chapter_url, chapter_title):
            chapter = {
                'url': self._base_url + url,
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
    d = {'name': '三寸人间', 'author': '耳根', 'url': 'http://www.biquge.com.tw/14_14055/'}
    num = 0
    for i in crawler.get_menu(d['name'], d['url']):
        num += 1
        i['num'] = num
        print(i)
    print(crawler.novel)
    # novel = next(crawler.get_info('xuanhuan'))
    # print(novel)
    # chapter = next(crawler.get_menu(novel['name'], novel['url']))
    # print(chapter)
    # content = crawler.get_chapter(chapter['url'])
    # print(content)
