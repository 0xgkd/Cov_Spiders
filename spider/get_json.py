#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: get_json.py
@time: 2021/1/24 18:39
@software: PyCharm 2020.1.2(Professional Edition)
'''

from tqdm import tqdm  # 进度条库
import json  # json格式处理
import time
import requests  # http请求库


# 获得世界疫情的json数据
def getCountryJson():
    # 读取数据
    with open("../data/worldData.json", 'r', encoding='utf-8') as f:
        countryJson = json.load(f)  # json格式加载
    # print(countryJson)
    print(f"{time.asctime()} 正在获取世界疫情的json数据...")
    time.sleep(0.8)
    str1 = "--"
    print(str1*50 + "世界各国疫情数据" + str1*50)
    for i in tqdm(range(0, len(countryJson)), ncols=50):
        print(
            "  " + f"{time.asctime()} " + "名称：" + countryJson[i]['provinceName'] + "  " +
            "代码：" + countryJson[i]['countryShortCode'] + "  " +
            "英文名：" + countryJson[i]['countryFullName'] + "  " +
            "疫情数据：" + countryJson[i]['statisticsData']
        )
        time.sleep(0.1)
        print()
    return countryJson


'''
处理世界世界疫情json数据，获得对应每一个国家的疫情json数据
'''
def handleCountryJson():
    countryJson = getCountryJson()
    errorNum = 0  # 统计出现爬取错误的数据数量
    num = 0  # 统计爬取成功的数据数量
    print(f"{time.asctime()} 开始爬取世界各国数据...")
    time.sleep(1.0)
    # print(len(countryJson))
    for i in tqdm(range(0, len(countryJson)), ncols=80):
        provinceName = countryJson[i]['provinceName']
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/87.0.4280.88 Safari/537.36'
            }

            res = requests.get(countryJson[i]['statisticsData'], headers=header)
            res.encoding = 'utf-8'
            everyCountryJson = res.text
            # print(everyCountryJson)
            path = "../data/worldData/" + provinceName + ".json"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(everyCountryJson)
            print("\t" + f"{time.asctime()} " + provinceName + "  数据已获取！")
            num += 1
            time.sleep(0.5)
        except:
            errorNum += 1
            print("\t" + f"{time.asctime()} 在获取  " + provinceName + "  数据时出错！")
    print(f"{time.asctime()}  世界各国数据获取完成！")
    print(f"{time.asctime()}  成功获取的数据量为：" + str(num) + " 条")
    print(f"{time.asctime()}  获取失败的数据量为：" + str(errorNum) + " 条")
    print()


# 获得国内疫情的json数据
def getProvinceJson():
    with open("../data/chinaData.json", 'r', encoding='utf-8') as f:
        provinceJson = json.load(f)
    print(f"{time.asctime()} 正在获取国内疫情的json数据...")
    time.sleep(0.8)
    str1 = "--"
    print(str1 * 48 + "中国各省疫情数据" + str1 * 48)
    for i in tqdm(range(0, len(provinceJson)), ncols=50):
        print(
            "\t" + f"{time.asctime()} " + "省份名称：" + provinceJson[i]['provinceName'] + "\t" +
            "省份简称：" + provinceJson[i]['provinceShortName'] + "\t" +
            "疫情数据：" + provinceJson[i]['statisticsData']
        )
        time.sleep(0.1)
        print()
    return provinceJson


# 获取各个省份对应的json数据
def handleProvinceJson():
    provinceJson = getProvinceJson()
    num = 0  # 统计爬取成功的数据数量
    errorNum = 0  # 统计出现爬取错误的数据数量
    print(f"{time.asctime()} 开始爬取国内各省份数据...")
    time.sleep(1.0)
    for i in tqdm(range(0, len(provinceJson)), ncols=80):
        provinceName = provinceJson[i]['provinceName']
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/87.0.4280.88 Safari/537.36'
            }
            res = requests.get(provinceJson[i]['statisticsData'], headers=header)
            res.encoding = 'utf-8'
            everyProvinceJson = res.text
            path = "../data/chinaData/" + provinceName + ".json"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(everyProvinceJson)
            print("\t" + f"{time.asctime()} " + provinceName + "  数据已获取！")
            num += 1
            time.sleep(0.8)
        except:
            errorNum += 1
            print("\t" + f"{time.asctime()} 在获取  " + provinceName + "  数据时出错！")
    print(f"{time.asctime()}  国内各省份数据获取完成！")
    print(f"{time.asctime()}  成功获取的数据量为：" + str(num) + " 条")
    print(f"{time.asctime()}  获取失败的数据量为：" + str(errorNum) + " 条")


# 程序入口
if __name__ == '__main__':
    handleCountryJson()
    handleProvinceJson()
