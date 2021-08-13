#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: get_hot.py
@time: 2021/1/27 19:01
@software: PyCharm 2020.1.2(Professional Edition)
'''

from selenium.webdriver import Chrome  # 调用chrome浏览器的底层接口来操作浏览器
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
import time
from tqdm import tqdm
import pymysql


# 获得百度疫情热搜
def getBaiduHot(url):
    option = ChromeOptions()  # 初始化chrome浏览器属性
    # 添加启动属性
    option.add_argument("--headless")  # 隐藏浏览器
    option.add_argument("--no-sandbox")  # 提前配置好后续在Linux上的部署需要参数

    browser = Chrome(options=option)  # 启动浏览器
    # browser = Chrome()
    # print(browser.page_source)
    try:
        browser.get(url)  # 发送url请求
        # 采用CSS选择器，根据元素层级进行定位，获取查看全部按钮
        but = browser.find_element_by_css_selector('#ptab-1 > div.Virus_1-1-315_2SKAfr > div.Common_1-1-315_3lDRV2')
        but.click()  # 点击展开
        time.sleep(1)  # 等待一秒

        # 采用xpath语法，一级一级节点，定位热搜的时间
        hotTime = browser.find_elements_by_xpath('//*[@id="ptab-1"]/div[3]/div/div[1]')
        # 定位热搜的内容
        hotContent = browser.find_elements_by_xpath('//*[@id="ptab-1"]/div[3]/div/div[2]/a/div')
        # print(type(hotContent))

        content = []  # 热搜列表
        for i in tqdm(range(0, len(hotTime)), ncols=80):
            content.append(hotTime[i].text)  # 添加热搜时间
            content.append(hotContent[i].text)  # 添加热搜内容
        # print(list1)

        count = 0
        for i in tqdm(range(0, len(hotContent)), ncols=70):
            count += 1  # 计数
            print(f"{time.asctime()}  " + "爬取的第 " + str(i+1) +" 条热搜： " + "2021年" + content[2*i] + " " + content[2*i+1])
            time.sleep(0.3)
        print(f"{time.asctime()}  共爬取疫情热搜：" + str(count) + " 条\n")
    except:
        print(f"{time.asctime()}  爬取疫情热搜出现错误！\n")
    browser.close()

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

    deleteSql = "truncate baidu"
    try:
        cursor.execute(deleteSql)  # 执行sql语句
        con.commit()
        print(f"{time.asctime()}  删除百度疫情热搜成功！正在进行重新导入...")
        time.sleep(3)
    except:
        print(f"{time.asctime()}  删除百度疫情热搜出错！正在进行回滚操作...")
        con.rollback()
        time.sleep(3)

    try:
        sql = "insert into baidu(datetime, comment) values('%s', '%s')"
        for i in tqdm(range(0, len(hotContent)), ncols=80):
            cursor.execute(sql % (content[2*i], content[2*i+1]))  # 插入数据
            # print(tuple(content[2*i]))
            time.sleep(0.1)
        con.commit()  # 提交事务保存数据
        print(f"{time.asctime()}  数据写入完毕!")
    except:
        print(f"{time.asctime()}  数据写入失败!")
        con.rollback()


# 程序入口
if __name__ == '__main__':
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia?fraz=partner&paaz=gjyj"
    getBaiduHot(url)  # 调用函数
