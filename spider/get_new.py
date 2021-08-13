#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: get_new.py
@time: 2021/1/26 20:05
@software: PyCharm 2020.1.2(Professional Edition)
'''

import requests
import json
import time
import pymysql
from tqdm import tqdm


def getChinaHtml(url):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }
        res = requests.get(url, headers=header)  # 发送http请求
        res.encoding = "utf-8"
        print(f"{time.asctime()}  获得腾讯疫情网页内容成功！")
        time.sleep(1.5)
        return res.text
    except:
        return f"{time.asctime()}  获得腾讯疫情页面内容出现错误！"


def importChinaDay(url):
    html = getChinaHtml(url)
    data = json.loads(html)
    # # 写个循环遍历到省级
    # count = 0
    # for i in data["areaTree"][0]["children"]:
    #     print(i["name"]) # 拿到各省名字
    #     count += 1
    # print(count)
    chinaData = json.loads(data["data"])

    # 建立数据库连接
    con = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        database="covid-19",
        charset='utf8'
    )

    # 使用cursor()方法创建一个游标对象cursor
    cursor = con.cursor()

    deleteSql = "truncate china_day"
    try:
        cursor.execute(deleteSql)
        con.commit()
        print(f"{time.asctime()}  删除国内昨日数据成功！正在更新数据...")
        time.sleep(3)
    except:
        print(f"{time.asctime()}  删除国内昨日数据出错！正在进行回滚操作...")
        con.rollback()
        time.sleep(3)

    dataList = []
    temp = ()
    temp += (
            int(chinaData["chinaTotal"]["confirm"]), int(chinaData["chinaTotal"]["heal"]),
            int(chinaData["chinaTotal"]["dead"]), int(chinaData["chinaTotal"]["nowConfirm"]),
            int(chinaData["chinaTotal"]["importedCase"]), int(chinaData["chinaTotal"]["localConfirm"])
        )
    dataList.append(temp)

    # 插入数据SQL
    insertSql = "INSERT INTO china_day(confirm, heal, dead, nowConfirm, importedCase, localConfirm) " \
                "VALUES(%s, %s, %s, %s, %s, %s)"
    # for char in tqdm(['.', '..', '...'], ncols=80):
    #     print("" + char)
    #     time.sleep(3)
    # 执行数据插入
    try:
        cursor.executemany(insertSql, dataList)
        con.commit()
        print(f"{time.asctime()}  保存国内最新疫情统计数据成功！")
    except:
        print(f"{time.asctime()}  保存国内最新疫情统计数据失败！正在进行回滚操作...")
        con.rollback()
    # 关闭连接
    cursor.close()
    con.close()


# 程序入口
if __name__ == '__main__':
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    importChinaDay(url)
