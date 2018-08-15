# coding=utf-8
from datetime import datetime

from lxml import etree
from app.utils.parse_url import parse_url
from app.database import MongodbClient


class CrawlBiquge(object):
    """
    Biquge crawler
    source: http://www.biquge.com.tw/
    """
    def __init__(self):
        self._biquge = 'http://www.biquge.com.tw/{category}/'
        self._base_url = 'http://www.biquge.com.tw'
        self._novel_html = None
        self.crawl_time = datetime.now()
        self._params = {'Cookie': '__cdnuid=90921b0dc2a86a57c01f43334eeef3ce; __cdn_clearance=1534338582.899|0|bqEUCHPkqErOJh7o4V5vAS2HLlU%3D'}

    def _novel_state(self, update_info):
        """get novels state, judge this novel is finished or unfinished"""
        spt = list(map(int, update_info[5:].split('-')))
        update_time = datetime(spt[0], spt[1], spt[2])
        interval_days = (self.crawl_time - update_time).days
        state = '更新中' if interval_days < 7 else '完结'
        return state

    def get_url(self, category):
        """crawler all novels url according to category"""
        url = self._biquge.format(category=category)
        res = parse_url(url, 'gbk', params=self._params)
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
                'source_url': url,
                'name': name,
                'author': author
            }
            yield novel

    def get_info(self, novel_url):
        """crawler novel info"""
        res = parse_url(novel_url, 'gbk', params=self._params)
        html = etree.HTML(res)
        self._novel_html = html
        image = html.xpath('//*[@id="fmimg"]/img/@src')[0]
        intro = html.xpath('//*[@id="intro"]/p/text()')[0]
        update_info = html.xpath('//*[@id="info"]/p[3]/text()')[0]
        state = self._novel_state(update_info)
        info = {
            'image': self._base_url + image,
            'intro': intro,
            'state': state
        }
        return info

    def get_menu(self, url=None):
        """crawling novel menu"""
        if self._novel_html is not None:
            if url:
                res = parse_url(url, 'gbk', params=self._params)
                self._novel_html = etree.HTML(res)
            else: return False
        chapter_url = self._novel_html.xpath('//*[@id="list"]/dl/dd/a/@href')
        chapter_title = self._novel_html.xpath('//*[@id="list"]/dl/dd/a/text()')
        for url, title in zip(chapter_url, chapter_title):
            chapter = {
                'source_url': self._base_url + url,
                'title': title
            }
            yield chapter

    def get_chapter(self, chapter_url):
        """crawler chapter content"""
        res = parse_url(chapter_url, 'gbk', params=self._params)
        html = etree.HTML(res)
        content = html.xpath('//*[@id="content"]/text()')
        return ''.join(content)

    def __call__(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    import time
    db = MongodbClient('novel', 'localhost', 27017)
    crawler = CrawlBiquge()
    cates = ['xuanhuan', 'xiuzhen', 'dushi', 'lishi', 'wangyou', 'kehuan', 'kongbu']
    for category in cates:
        for novel in crawler.get_url(category):
            db.change_table('novel')
            novel['category'] = category
            info = crawler.get_info(novel['source_url'])
            data = dict(novel, **info)
            print('success novel: ', data['source_url'])
            db.put(data)
            db.change_table('chapter')
            for c in crawler.get_menu(novel['source_url']):
                if db.exists({'novel': novel['name'], 'title': c['title']}):
                    continue
                time.sleep(1)
                try:
                    content = crawler.get_chapter(c['source_url'])
                    c['content'] = content
                    c['novel'] = novel['name']
                    c['author'] = novel['author']
                    print('success chapter: ', c['source_url'])
                    db.put(c)
                except:
                    db.change_table('errors')
                    db.put(c)
                    db.change_table('chapter')



