import json
from collections import defaultdict
from random import randint

import unicodedata

idiom_datas: list
idiom_first_pinyin_dict = defaultdict(list)


def _processing_tone(pinyin: str) -> str:
    return str(unicodedata.normalize('NFKD', pinyin).encode('ascii', 'ignore'), 'UTF-8')


def __init__():
    with open("idiom.json", 'r', encoding='utf8') as fp:
        global idiom_datas
        idiom_datas = json.load(fp)
        for idiom in idiom_datas:
            pinyin: str
            pinyin = idiom['pinyin']
            pinyin_len = len(pinyin.split(' '))
            # 只使用四字成语
            if pinyin_len == 4:
                first_pinyin = pinyin.split(' ')[0]
                # 同音不同声也可以接下去
                first_pinyin = _processing_tone(first_pinyin)
                idiom_first_pinyin_dict[first_pinyin].append(idiom)


def find_idiom_by_all_word(word: str) -> dict:
    for idiom in idiom_datas:
        if word == idiom['word']:
            return idiom


def get_idiom_first_pinyin(idiom: dict) -> str:
    pinyin: str
    pinyin = idiom['pinyin']
    return _processing_tone(pinyin.split(' ')[0])


def get_idiom_end_pinyin(idiom: dict) -> str:
    pinyin: str
    pinyin = idiom['pinyin']
    return _processing_tone(pinyin.split(' ')[-1])


if __name__ == '__main__':
    __init__()
    begin_idiom_word = input("请输入开始的成语:\n")
    begin_idiom = find_idiom_by_all_word(begin_idiom_word)
    if begin_idiom is None:
        print(f'没有找到该成语：{begin_idiom_word}')
        exit()
    result_str = ''
    result_str += begin_idiom['word']
    # 一直循环知道找不到可以接的成语
    while True:
        # 将本次找到的成语从字典中删除
        idiom_first_pinyin_dict[get_idiom_first_pinyin(begin_idiom)].remove(begin_idiom)
        current_idiom_end_pinyin = get_idiom_end_pinyin(begin_idiom)
        idioms = idiom_first_pinyin_dict[current_idiom_end_pinyin]
        if len(idioms) > 0:
            # 从符合的结果中随机取一个成语
            begin_idiom = idioms[randint(0, len(idioms) - 1)]
            result_str += '->' + begin_idiom['word']
            # 每一百个字符输出一次
            if len(result_str) > 100:
                print(result_str)
                result_str = ''
        else:
            print(result_str)
            print('竟然找不到可以接的成语了呢！')
            exit()
