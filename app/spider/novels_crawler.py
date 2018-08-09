# coding=utf-8
from lxml import etree
from app.utils.parse_url import parse_url


class CrawlMetaclass(type):
    """
    add __CrawlFunc__ and __CrawlFuncCount__ attr
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k in attrs.keys():
            if k.startswith('crawl_'):
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class NovelCrawler(object, metaclass=CrawlMetaclass):

    def __init__(self, **kwargs):
        self._qidian = 'https://www.qidian.com/search?kw={keyword}'
        self._biquge = 'http://www.biquge.com.tw/{category}/'
        super(NovelCrawler, self).__init__(**kwargs)

    def get_raw_vovels(self, callback):
        novels = []
        for novel in eval("self.{}()".format(callback)):
            print('Getting', novel, 'from', callback)
            novels.append(novel)
        return novels

    def crawl_qidian(self, keyword):
        """起点网"""
        pass

    def crawl_biquge(self, category):
        """笔趣阁"""
        url = self._biquge.format(category=category)
        print(url)
        res = parse_url(url, 'gbk')
        print(res)
        html = etree.HTML(res)
        hot_divs = html.xpath('//*[@id="hotcontent"]/div[@class="ll"]/div[@class="item"]')[0]
        hot_href = hot_divs.xpath('//div[@class="image"]/a/@href')
        hot_image = hot_divs.xpath('//div[@class="image"]/a/img/@src')
        hot_name = hot_divs.xpath('//dl/dt[1]/a/text()')
        hot_author = hot_divs.xpath('//dl/dt/span/text()')
        hot_info = hot_divs.xpath('//dl/dd/text()')
        l = []
        for href, image, name, author, info in zip(hot_href, hot_image, hot_name, hot_author, hot_info):
            novel = {
                'href': href,
                'image': image,
                'name': name,
                'author': author,
                'info': info.strip()
            }
            l.append(novel)
        print(l)
    def crawl_xxsy(self):
        """潇湘书院"""
        pass

    def crawl_zongheng(self):
        """纵横"""
        pass


if __name__ == '__main__':
    NovelCrawler().crawl_biquge('xuanhuan')
