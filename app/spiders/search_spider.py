# coding=utf-8
from lxml import etree
from app.utils.parse_url import parse_url


class SearchMetaclass(type):
    """
    add __CrawlFunc__ and __CrawlFuncCount__ attr
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__SearchFunc__'] = []
        for k in attrs.keys():
            if k.startswith('search_'):
                attrs['__SearchFunc__'].append(k)
                count += 1
        attrs['__SearchFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class SearchCrawler(object, metaclass=SearchMetaclass):

    def __init__(self, **kwargs):
        self._qidian = 'https://www.qidian.com/search?kw={keyword}'
        self._biquge = 'http://www.biquge.com.tw/{category}/'
        super(SearchCrawler, self).__init__(**kwargs)

    def get_raw_vovels(self, callback):
        novels = []
        for novel in eval("self.{}()".format(callback)):
            print('Getting', novel, 'from', callback)
            novels.append(novel)
        return novels

    def search_qidian(self, keyword):
        """起点网"""
        pass

    def search_biquge(self, category):
        """笔趣阁"""
        pass

    def search_xxsy(self):
        """潇湘书院"""
        pass

    def search_zongheng(self):
        """纵横"""
        pass


if __name__ == '__main__':
    SearchCrawler().search_biquge('xuanhuan')
