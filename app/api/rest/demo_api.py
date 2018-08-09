from flask import request, jsonify

from app.api import api_bp

temp = [{'name': '圣墟', 'image': 'http://www.biquge.com.tw/files/article/image/11/11850/11850s.jpg', 'info': '在破败中崛起，在寂灭中复苏。沧海成尘，雷电枯竭……...', 'href': 'http://www.biquge.com.tw/11_11850/', 'author': '辰东'}, {'name': '牧神记', 'image': 'http://www.biquge.com.tw/files/article/image/6/6595/6595s.jpg', 'info': '大墟的祖训说，天黑，别出门。\u3000\u3000大墟残老村的老弱病残们从江边捡到了一个婴儿，取名秦牧，含辛茹苦将他养大。这一天夜幕降临，黑暗笼罩大墟，秦牧走出了家门……\u3000\u3000做个春风中...', 'href': 'http://www.biquge.com.tw/6_6595/', 'author': '宅猪'}, {'name': '噬元之主', 'image': 'http://www.biquge.com.tw/files/article/image/0/396/396s.jpg', 'info': '不知是命运的作弄，还是幕后黑手的布局，通过一场举世震惊的地震，\n    一个懵懂的少年，就这么穿越到了这个神奇的世界。\n    在这里，人们以武为尊！\n    在这里，强者可以践踏弱...', 'href': 'http://www.biquge.com.tw/0_396/', 'author': '失心至尊'}, {'name': '诛仙神尊', 'image': 'http://www.biquge.com.tw/files/article/image/16/16185/16185s.jpg', 'info': '剑道传人，逆天之上，碎虚空，斩修界，叱咤十方！     剑气纵横三万里，一剑光寒御九霄！     一代剑道宗师独孤求败后代，携家族传承之剑，一人一剑，神挡杀神，魔挡杀魔！     诛...', 'href': 'http://www.biquge.com.tw/16_16185/', 'author': '深海浮冰'}, {'name': '斗战狂潮', 'image': 'http://www.biquge.com.tw/files/article/image/0/703/703s.jpg', 'info': '双月当空，无限可能的英魂世界     孤寂黑暗，神秘古怪的嬉命小丑     百城联邦，三大帝国，异族横行，魂兽霸幽     这是一个英雄辈出的年代，人类卧薪尝胆重掌地球主权，孕育着进...', 'href': 'http://www.biquge.com.tw/0_703/', 'author': '骷髅精灵'}, {'name': '异世邪君', 'image': 'http://www.biquge.com.tw/files/article/image/1/1421/1421s.jpg', 'info': '世间毁誉，世人冷眼，与我何干？我自淡然一笑；\n    以吾本性，快意恩仇，以吾本心，遨游世间，我命由我不由天！\n    一代牛人穿越异界，看其如何踏上异世巅峰，成为一代邪君！\n ...', 'href': 'http://www.biquge.com.tw/1_1421/', 'author': '风凌天下'}]

# /api/test?num=2
@api_bp.route('/test')
def api_test():
    counts = len(temp)
    # print(counts)
    num = request.args.get('num', 1, type=int)
    if num < counts:
        return jsonify(temp[num])
    return jsonify({'msg': 'error'})
