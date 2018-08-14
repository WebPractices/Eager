# coding=utf-8
from datetime import datetime

from lxml import etree
from app.utils.parse_url import parse_url
from app.database import MongodbClient


class CrawlXs147(object):
    """
    147xs crawler
    source: http://www.147xs.com/
    """

    def __init__(self):
        self._base_url = 'http://www.147xs.com'
        self._xs147 = 'http://www.147xs.com/sort/{category}/'
        self._novel_html = None
        self.crawl_time = datetime.now()

    def _novel_state(self, update_info):
        """get novels state, judge this novel is finished or unfinished"""
        spt = list(map(int, update_info.split('-')))
        update_time = datetime(spt[0], spt[1], spt[2])
        interval_days = (self.crawl_time - update_time).days
        state = '更新中' if interval_days < 7 else '完结'
        return state

    def get_url(self, category):
        """crawler all novels url according to category"""
        url = self._xs147.format(category=category)
        res = parse_url(url, 'utf-8')
        html = etree.HTML(res)
        urls = html.xpath('//*[@id="main"]/div[@class="novelslist"]/div[1]/ul/li/a/@href')
        names = html.xpath('//*[@id="main"]/div[@class="novelslist"]/div[1]/ul/li/a/text()')
        authors = html.xpath('//*[@id="main"]/div[@class="novelslist"]/div[1]/ul/li/text()')
        for url, name, author in zip(urls, names, authors):
            novel = {
                'source_url': url,
                'name': name,
                'author': author.lstrip('/')
            }
            yield novel

    def get_info(self, novel_url):
        """crawler novel info"""
        res = parse_url(novel_url, 'utf-8')
        html = etree.HTML(res)
        self._novel_html = html
        image = html.xpath('//*[@id="fmimg"]/a/img/@src')[0]
        intro = html.xpath('//*[@id="intro"]/text()')[2]
        update_info = html.xpath('//*[@id="info"]/p[3]/text()')[0]
        _datetime = update_info.split('：')[1].split(' ')[0]
        state = self._novel_state(_datetime)
        info = {
            'image': self._base_url + image,
            'intro': intro,
            'state': state
        }
        return info

    def get_menu(self, url=None):
        """crawling novel menu"""
        if self._novel_html is None:
            if url:
                res = parse_url(url, 'utf-8')
                self._novel_html = etree.HTML(res)
            else: return False
        chapter_url = self._novel_html.xpath('//*[@id="list"]/dd/a/@href')
        chapter_title = self._novel_html.xpath('//*[@id="list"]/dd/a/text()')
        for url, title in zip(chapter_url, chapter_title):
            chapter = {
                'source_url': self._base_url + url,
                'title': title
            }
            yield chapter

    def get_chapter(self, chapter_url):
        """crawler chapter content"""
        res = parse_url(chapter_url, 'utf-8')
        html = etree.HTML(res)
        content = html.xpath('//*[@id="content"]/p/text()')
        return '\n'.join(content)

if __name__ == '__main__':
    import time

    db = MongodbClient('novel', 'localhost', 27017)
    crawler = CrawlXs147()
    cates = {
        '1': 'xuanhuan',
        '2': 'xiuzhen',
        '3': 'dushi',
        '4': 'lishi',
        '5': 'zhichang',
        '6': 'wangyou',
        '7': 'kehuan',
        '8': 'junshi',
        '9': 'lingyi',
        '10': 'qihuan',
        '11': 'wuxia',
        '12': 'jingji',
        '13': 'tongren',
        '14': 'yanqing'
    }
    for category, value in cates.items():
        for novel in crawler.get_url(category):
            db.change_table('novel')
            novel['category'] = value
            info = crawler.get_info(novel['source_url'])
            data = dict(novel, **info)
            print('success novel: ', data['source_url'])
            db.put(data)
            db.change_table('chapter')
            for c in crawler.get_menu(novel['source_url']):
                time.sleep(1)
                content = crawler.get_chapter(c['source_url'])
                c['content'] = content
                c['novel'] = novel['name']
                c['author'] = novel['author']
                print('success chapter: ', c['source_url'])
                db.put(c)

