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
from bs4 import BeautifulSoup


def refreshTKK():
    headers = {
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    }

    url = 'https://translate.google.cn/'

    try:
        resultPage = request.urlopen(request.Request(url, headers=headers))

    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    except Exception as e:
        print('translate error.')
        print(e)

    # 取得翻译的结果，翻译的结果是json格式
    resultJason = resultPage.read()
    soup = BeautifulSoup(resultJason, "html.parser")
    allinfo = soup.find_all('script')
    for info in allinfo:
        chinese = info.get_text()

        if chinese.find("TKK") > 0:
            res = chinese.split("TKK")[1]
            res = res.split(");")[0]
            ttk = open('getTKK.js', 'w')
            ttk.write("TKK" + res + ");\n")
            ttk.write("console.log(TKK);")
            ttk.close()
            os.system('node getTKK.js > TKK')
            tkk = open('TKK', 'r')
            TKK = tkk.read().replace('\n', '')
            tkk.close()
            return TKK
