from flask import request, jsonify

from app.api import api_bp
from app.spiders import CrawlBiquge

temp = [{'name': '圣墟', 'url': 'http://www.biquge.com.tw/11_11850/', 'author': '辰东'}, {'name': '牧神记', 'url': 'http://www.biquge.com.tw/6_6595/', 'author': '宅猪'}, {'name': '噬元之主', 'url': 'http://www.biquge.com.tw/0_396/', 'author': '失心至尊'}, {'name': '诛仙神尊', 'url': 'http://www.biquge.com.tw/16_16185/', 'author': '深海浮冰'}, {'name': '斗战狂潮', 'url': 'http://www.biquge.com.tw/0_703/', 'author': '骷髅精灵'}, {'name': '异世邪君', 'url': 'http://www.biquge.com.tw/1_1421/', 'author': '风凌天下'}]
temp_menu = []
with open('menu.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        # print(i)
        temp_menu.append(eval(i))
novel_cache = {}
menu_cache = {}
content_cache = {}

@api_bp.route('/novels')
def novels_test():
    if temp:
        return jsonify({'novels': temp})
    return jsonify({'msg': 'error'})

# /api/novel?num='圣墟'
@api_bp.route('/novel')
def novel_test():
    name = request.args.get('name', '圣墟', type=str)
    if novel_cache.get(name):
        return jsonify(novel_cache[name])
    url = ''
    author = ''
    for i in temp:
        if name == i['name']:
            url = i['url']
            author = i['author']
            break
    if url:
        bqgCrawler = CrawlBiquge()
        info = bqgCrawler.get_info(name, url)
        info['category'] = '玄幻'
        info['name'] = name
        info['author'] = author
        novel_cache[name] = info
        return jsonify(info)
    return jsonify({'msg': 'no result'})

# /api/menu?novel='圣墟'
@api_bp.route('/menu')
def menu_test():
    name = request.args.get('name', '圣墟', type=str)
    if menu_cache.get(name):
        return jsonify(menu_cache[name])
    url = ''
    for i in temp:
        if name == i['name']:
            url = i['url']
            break
    if url:
        bqgCrawler = CrawlBiquge()
        menu = []
        for i in bqgCrawler.get_menu(name, url):
            menu.append(i)
        menu_cache[name] = menu
        return jsonify({'menu': menu})
    return jsonify({'msg': 'no result'})

# /api/chapter?num=1
@api_bp.route('/chapter')
def chapter_test():
    num = request.args.get('num', 1, type=int)
    if content_cache.get(str(num)):
        return jsonify(content_cache[str(num)])
    if num < 31:
        bqgCrawler = CrawlBiquge()
        url = temp_menu[num]['url']
        title = temp_menu[num]['title']
        content = bqgCrawler.get_chapter(url)
        data = {'chapter': title, 'content': content}
        content_cache[str(num)] = data
        return jsonify(data)
    return jsonify({'msg': 'no result'})
