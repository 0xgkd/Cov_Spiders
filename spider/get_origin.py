#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: get_origin.py
@time: 2021/1/24 14:19
@software: PyCharm 2020.1.2(Professional Edition)
'''

import requests  # http请求库
from bs4 import BeautifulSoup  # html解析库
import time


# 获取原始页面文本数据
def getOriginHtmlText(url):
    try:
        # 添加请求头
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }
        res = requests.get(url, headers=header)
        res.encoding = "utf-8"  # 设置编码
        print(f"{time.asctime()} 获得原始页面内容成功！")
        time.sleep(0.8)
        return res.text  # 返回页面文本
    except:
        return f"{time.asctime()} 获得原始页面内容出现错误！"


# 获取世界的疫情数据
def getWorldJsonText(url):
    html = getOriginHtmlText(url)  # 调用获取页面源码函数，得到页面源码文本
    soup = BeautifulSoup(html, features="lxml")  # BeautifulSoup调用lxml解析器
    # 处理数据
    str1 = str(soup.find_all('script', {"id": "getListByCountryTypeService2true"}))
    # 提取
    worldDataStr = str1[str1.find('[{'):str1.find('}catch')]
    # 写入世界数据文件
    with open("../data/worldData.json", "w", encoding='utf-8') as f:
        f.write(worldDataStr)
        print(f"{time.asctime()} 写入世界数据文件成功！")


# 获取国内的疫情数据
def getChinaJsonText(url):
    html = getOriginHtmlText(url)  # 调用获取页面源码函数，得到页面源码文本
    soup = BeautifulSoup(html, features="lxml")  # BeautifulSoup调用lxml解析器
    # 处理数据
    str2 = str(soup.find_all('script', {"id": "fetchRecentStat"}))
    # 提取
    chinaDataStr = str2[str2.find('[{'):str2.find('}catch')]
    # 写入国内数据文件
    with open("../data/chinaData.json", "w", encoding='utf-8') as f:
        f.write(chinaDataStr)
        print(f"{time.asctime()} 写入国内数据文件成功！")


# 程序入口
if __name__ == '__main__':
    url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
    getWorldJsonText(url)
    getChinaJsonText(url)
