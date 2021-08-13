#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: utils.py
@time: 2021/2/2 13:05
@software: PyCharm 2020.1.2(Professional Edition)
'''

import time
import pymysql
from flask import jsonify
import string
import jieba.analyse


# 时间函数
def flush_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


def open_con():
    # 建立数据库连接
    con = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        database="covid-19",
        charset='utf8'
    )
    # 使用cursor()方法创建一个游标对象cursor，返回结果集为元组形式
    cursor = con.cursor()
    return con, cursor


# 关闭连接
def close_con(con, cursor):
    cursor.close()
    con.close()


# 查询功能
def query(sql, *args):
    conn, cursor = open_con()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    close_con(conn, cursor)
    return result


# 查询累计确诊、累计治愈、累计死亡、现存确诊
def get_c1_data():
    sql = "select confirm, heal, dead, nowConfirm from china_day"
    res = query(sql)
    return res[0]


# 查询省份名称、累计确诊
def get_c2_data():
    sql = "select provinceShortName, confirmedCount from china_province " \
          "where dateID=(select dateID from china_province " \
          "order by dateID desc limit 1) group by provinceShortName"
    result = query(sql)
    return result
    # tup = utils.get_c2_data()
    # res = []
    # for i in range(len(result)):
    #     res.append({
    #         "name": result[i][0],
    #         "value": int(result[i][1])
    #     })
    # print(jsonify({"data": res}))
    # print(res)


# 查询累计确诊、累计治愈、累计死亡、现存确诊
def get_l1_data():
    sql = "select dateID, confirmedCount, curedCount, deadCount, currentConfirmedCount from china_total"
    res = query(sql)
    return res
    # print(res)
    # dateID, confirmedCount, curedCount, deadCount, currentConfirmedCount = [], [], [], [], []
    # for a, b, c, d, e in res:
    #     dateID.append(a)
    #     confirmedCount.append(b)
    #     curedCount.append(c)
    #     deadCount.append(d)
    #     currentConfirmedCount.append(e)
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(e)


# 查询新增确诊、新增治愈
def get_l2_data():
    sql = "select dateID, confirmedIncr, curedIncr from china_total"
    res = query(sql)
    return res


# 查询国家简称、累计确诊
def get_r1_data():
    sql = "select provinceName, currentConfirmedCount from (" \
          "select provinceName, currentConfirmedCount from world " \
          "where dateID=(select dateID from world order by dateID desc limit 1) " \
          "group by provinceName" \
          ") as a order by currentConfirmedCount desc limit 5"
    res = query(sql)
    return res


# 查询百度热搜
def get_r2_data():
    sql = "select comment from baidu order by datetime desc limit 20"
    res = query(sql)
    return res
    # print(type(res[0][0]))
    # print(res[0][0])
    # print(res[0][0].rstrip(string.digits))
    # print(res[0][0][len(res[0][0].rstrip(string.digits)):])
    # print(type(res[0][0].rstrip(string.digits)))
    # print(res[0][0].rstrip(string.digits))
    # for i in range(len(res)):
    #     item = res[i][0]
    #     jieba.analyse.set_stop_words('./static/baidu_stopwords.txt')
    #     keywords = jieba.analyse.extract_tags(item, topK=20, withWeight=True, allowPOS=())
    #     for k, v in keywords:
    #         print(k,v)


def get_world_data():
    sql = "select provinceName, confirmedCount from world where dateID=(select dateID from world " \
          "order by dateID desc limit 1) group by provinceName"
    res = query(sql)
    return res


# 调试入口
if __name__ == "__main__":
    # print(flush_time())
    # print(get_c1_data())
    print(get_c2_data())
    # print(get_l1_data())
    # print(get_l2_data())
    # print(get_r1_data())
    # print(get_r2_data())
    # print()
    # print(get_world_data())
    # flush_time()
