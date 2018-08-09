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

    def crawl_biquge(self):
        """笔趣阁"""
        pass

    def crawl_xxsy(self):
        """潇湘书院"""
        pass

    def crawl_zongheng(self):
        """纵横"""
        pass


if __name__ == '__main__':
    pass
