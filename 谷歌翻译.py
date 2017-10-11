#!/usr/bin/python
# coding:utf-8

import sys
import os
import json  # 导入json模块
import urllib  # 导入urllib模块
from urllib import request, parse
from urllib.error import URLError, HTTPError
import _md5
import datetime
from lxml import etree
import refreshTKK

TKK = refreshTKK.refreshTKK()


def translate(cnValue='english', tl='zh-CN'):
    global TKK
    os.system('node gettk.js > result ' + cnValue + ' ' + TKK)
    result = open('result', 'r')
    tk = result.read().replace('\n', '')
    result.close()

    headers = {
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    }
    q = parse.quote(cnValue)
    url = 'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=' + tl + \
        '&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=0&tsel=0&kc=0&tk=' + tk + '&q=' + q

    try:
        resultPage = request.urlopen(request.Request(url, headers=headers))
        # 取得翻译的结果，翻译的结果是json格式
        resultJason = resultPage.read().decode('utf-8')
        js = None
        try:
            # 将json格式的结果转换成Python的字典结构
            js = json.loads(resultJason)
            result = js[0][0][0]
            print('result: ' + result)
        except Exception as e:
            print('loads Json error.')
            print(e)
            result = cnValue
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        print('url: ', url)
        result = cnValue
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        print('url: ', url)
        result = cnValue
    except Exception as e:
        print('translate error.')
        print(e)
        print('url: ', url)
        result = cnValue
    return result


def iteratorElem(elememt):
    for sub in elememt:
        try:
            cnValue = sub.attrib['value3']
            sub.attrib['value4'] = translate(cnValue, 'zh-TW')
            sub.attrib['value5'] = translate(cnValue, 'ar')
            sub.attrib['value6'] = translate(cnValue, 'fr')
        except KeyError as e:
            pass
        finally:
            iteratorElem(sub)


if __name__ == '__main__':
    # 通过获得命令行参数获得输入输出文件名
    for rt, dirs, files in os.walk(os.getcwd() + os.sep):
        for f in files:
            if(not os.path.exists(os.getcwd() + os.sep + f)):
                continue
            fname = os.path.splitext(f)
            if fname[1].lower() == ".xml":
                tree = etree.parse(f)
                root = tree.getroot()
                iteratorElem(root)
                tree.write(f, encoding="UTF-8")
