#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: get_json.py
@time: 2021/1/25 20:12
@software: PyCharm 2020.1.2(Professional Edition)
'''

import pymysql
import json
from tqdm import tqdm
import time


def getNameDict():
    countryNameDict = {}
    path = "../data/worldData.json"
    with open(path, 'r', encoding='utf-8') as f:
        worldData = json.load(f)
    num = 0
    errorNum = 0
    for i in tqdm(range(0, len(worldData)), ncols=80):
        try:
            key = worldData[i]["provinceName"]
            value = worldData[i]["countryFullName"]
            countryNameDict[key] = value
            num += 1
            print(
                "\t" + f"{time.asctime()}  建立 " + worldData[i]["provinceName"]
                + "  和  " + worldData[i]["countryFullName"]
                + "  映射成功！\n"
            )
            time.sleep(0.1)
        except:
            errorNum += 1
            print(
                "\t" + f"{time.asctime()}  建立 " + worldData[i]["provinceName"]
                + "  和  " + worldData[i]["countryFullName"]
                + "  映射失败！\n"
            )
            time.sleep(0.1)
    time.sleep(0.3)
    print(f"{time.asctime()}  世界各国名称和英文名称的映射字典建立完成！")
    print(f"{time.asctime()}  映射成功数：", str(num))
    print(f"{time.asctime()}  映射失败数：", str(errorNum))
    print()
    return countryNameDict


# 将世界各国疫情数据写入数据库
def importWorldData():
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

    deleteSql = "truncate world"
    try:
        cursor.execute(deleteSql)
        con.commit()
        print(f"{time.asctime()}  删除世界各国疫情数据成功！正在进行重新导入...")
        time.sleep(1.0)
    except:
        print(f"{time.asctime()}  删除世界各国疫情数据出错！正在进行回滚操作...")
        con.rollback()
        time.sleep(1.0)
    path = "../data/worldData.json"
    with open(path, 'r', encoding='utf-8') as f:
        worldData = json.load(f)

    countryNameDict = getNameDict()
    # 批量插入的数据集合
    insertValue = []
    # 所插入的主键记录
    dataCountWorld = 1
    print(f"{time.asctime()}  正在保存世界各国疫情数据...")
    time.sleep(1.3)
    for i in tqdm(range(0, len(worldData)), ncols=80):
        # 获取每一个国家的名称，并打开其对应的json文件
        continent = worldData[i]['continents']
        countryName = worldData[i]['provinceName']
        countryShortCode = worldData[i]['countryShortCode']
        countryFullName = countryNameDict[worldData[i]['provinceName']]

        countryJsonPath = "../data/worldData/" + countryName + ".json"
        with open(countryJsonPath, "r", encoding='utf-8') as f:
            countryJson = json.load(f)
        i += 1
        for j in range(0, len(countryJson['data'])):
            tupleWorldData = ()
            tupleWorldData += (
                dataCountWorld, continent, countryName, countryShortCode, countryFullName,
                countryJson['data'][j]['confirmedCount'], countryJson['data'][j]['confirmedIncr'],
                countryJson['data'][j]['curedCount'], countryJson['data'][j]['curedIncr'],
                countryJson['data'][j]['currentConfirmedCount'], countryJson['data'][j]['currentConfirmedIncr'],
                countryJson['data'][j]['dateId'], countryJson['data'][j]['deadCount'],
                countryJson['data'][j]['deadIncr'], countryJson['data'][j]['highDangerCount'],
                countryJson['data'][j]['midDangerCount'], countryJson['data'][j]['suspectedCount'],
                countryJson['data'][j]['suspectedCountIncr']
            )
            insertValue.append(tupleWorldData)
            dataCountWorld += 1

    insertSql = "INSERT INTO world(id, continents, provinceName, countryShortCode, countryFullName, " \
                    "confirmedCount, confirmedIncr, curedCount, curedIncr, currentConfirmedCount, " \
                "currentConfirmedIncr, dateId, deadCount, deadIncr, highDangerCount, midDangerCount, suspectedCount, " \
                "suspectedCountIncr) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # 执行数据插入
    try:
        cursor.executemany(insertSql, insertValue)
        con.commit()
        print(f"{time.asctime()}  保存世界各国疫情数据成功！")
        print(f"{time.asctime()}  共保存数据：" + str(dataCountWorld-1) + " 条")
        print()
    except:
        print(f"{time.asctime()}  保存世界各国疫情数据失败！正在进行回滚操作...")
        print()
        con.rollback()
    # 关闭连接
    cursor.close()
    con.close()


# 将国内各省数据疫情数据写入数据库
def importChinaData():
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

    deleteSql = "truncate china"
    try:
        cursor.execute(deleteSql)
        con.commit()
        print(f"{time.asctime()}  删除国内各省份疫情数据成功！正在进行重新导入...")
        time.sleep(1.0)
    except:
        print(f"{time.asctime()}  删除国内各省份疫情数据出错！正在进行回滚操作...")
        con.rollback()
        time.sleep(1.0)
    path = "../data/chinaData.json"
    with open(path, 'r', encoding='utf-8') as f:
        provinceData = json.load(f)

    # 批量插入的数据集合
    insertValue = []
    # 所插入的主键记录
    dataCountProvince = 1
    for i in tqdm(range(0, len(provinceData)), ncols=80):
        # 获取每一个省份的名称，并打开其对应的json文件
        provinceName = provinceData[i]['provinceName']
        provinceShortName = provinceData[i]['provinceShortName']

        provinceJsonPath = "../data/chinaData/" + provinceName + ".json"
        with open(provinceJsonPath, 'r', encoding='utf-8') as f:
            provinceJson = json.load(f)
        i += 1
        for j in range(0, len(provinceJson['data'])):
            tupleChinaData = ()
            tupleChinaData += (
                dataCountProvince, provinceName, provinceShortName, provinceJson['data'][j]['confirmedCount'],
                provinceJson['data'][j]['confirmedIncr'], provinceJson['data'][j]['curedCount'],
                provinceJson['data'][j]['curedIncr'], provinceJson['data'][j]['currentConfirmedCount'],
                provinceJson['data'][j]['currentConfirmedIncr'], provinceJson['data'][j]['dateId'],
                provinceJson['data'][j]['deadCount'], provinceJson['data'][j]['deadIncr'],
                provinceJson['data'][j]['highDangerCount'], provinceJson['data'][j]['midDangerCount'],
                provinceJson['data'][j]['suspectedCount'], provinceJson['data'][j]['suspectedCountIncr']
            )
            insertValue.append(tupleChinaData)
            dataCountProvince += 1

    insertSql = "INSERT INTO china(id, provinceName, provinceShortName, confirmedCount, confirmedIncr, curedCount, " \
                "curedIncr, currentConfirmedCount, currentConfirmedIncr, dateId, deadCount, deadIncr, " \
                "highDangerCount, midDangerCount, suspectedCount, suspectedCountIncr) " \
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        cursor.executemany(insertSql, insertValue)
        con.commit()
        print(f"{time.asctime()}  保存国内各省份疫情数据成功！")
        print(f"{time.asctime()}  共保存数据：" + str(dataCountProvince-1) + " 条")
        print()
    except:
        print(f"{time.asctime()}  保存国内各省份疫情数据失败！正在进行回滚操作...")
        con.rollback()
        print()
    # 关闭连接
    cursor.close()
    con.close()


# 统计世界总体疫情数据
def importWorldTotalData():
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

    deleteSql = "truncate world_total"
    try:
        cursor.execute(deleteSql)
        con.commit()
        print(f"{time.asctime()}  删除世界疫情数据成功！正在进行重新导入...")
        time.sleep(1.0)
    except:
        print(f"{time.asctime()}  删除世界疫情数据出错！正在进行回滚操作...")
        con.rollback()
        time.sleep(1.0)

    querySql = "select sum(confirmedCount), sum(confirmedIncr), sum(curedCount), sum(curedIncr), " \
               "sum(currentConfirmedCount), sum(currentConfirmedIncr), dateId, sum(deadCount), sum(deadIncr), " \
               "sum(highDangerCount), sum(midDangerCount), sum(suspectedCount), sum(suspectedCountIncr) from world " \
               "group by dateId order by dateId"
    cursor.execute(querySql)
    queryList = cursor.fetchall()

    dataList = []
    idWorld = 1
    for data in tqdm(queryList, ncols=80):
        temp = ()
        temp += (
            idWorld, int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]),
            int(data[7]), int(data[8]), int(data[9]), int(data[10]), int(data[11]), int(data[12])
        )
        dataList.append(temp)
        idWorld += 1

    # print(dataList)
    # 插入数据SQL
    insertSql = "INSERT INTO world_total(id, confirmedCount, confirmedIncr, curedCount, curedIncr, " \
                "currentConfirmedCount, currentConfirmedIncr, dateId, deadCount, deadIncr, highDangerCount, " \
                "midDangerCount, suspectedCount, suspectedCountIncr) " \
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.executemany(insertSql, dataList)
        con.commit()
        time.sleep(1.2)
        print(f"{time.asctime()}  保存世界总体疫情数据成功！")
        time.sleep(0.2)
        print(f"{time.asctime()}  共保存数据：" + str(idWorld-1) + " 条")
        print()
    except:
        time.sleep(1.2)
        print(f"{time.asctime()}  保存世界总体疫情数据失败！正在进行回滚操作...")
        con.rollback()
        print()
    # 关闭连接
    cursor.close()
    con.close()


# 统计国内总体疫情数据
def importChinaTotalData():
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

    deleteSql = "truncate china_total"
    try:
        cursor.execute(deleteSql)
        con.commit()
        print(f"{time.asctime()}  删除国内数据成功！正在进行重新导入...")
        time.sleep(1)
    except:
        print(f"{time.asctime()}  删除国内数据出错！正在进行回滚操作...")
        con.rollback()
        time.sleep(1)

    querySql = "select sum(confirmedCount), sum(confirmedIncr), sum(curedCount), sum(curedIncr), " \
               "sum(currentConfirmedCount), sum(currentConfirmedIncr), dateId, sum(deadCount), sum(deadIncr), " \
               "sum(highDangerCount), sum(midDangerCount), sum(suspectedCount), sum(suspectedCountIncr) from china " \
               "group by dateId order by dateId"
    cursor.execute(querySql)
    queryList = cursor.fetchall()

    dataList = []
    idChina = 1
    for data in tqdm(queryList, ncols=80):
        temp = ()
        temp += (
            idChina, int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]),
            int(data[7]), int(data[8]), int(data[9]), int(data[10]), int(data[11]), int(data[12])
        )
        dataList.append(temp)
        idChina += 1

    # print(dataList)
    # 插入数据SQL
    insertSql = "INSERT INTO china_total(id, confirmedCount, confirmedIncr, curedCount, curedIncr, " \
                "currentConfirmedCount, currentConfirmedIncr, dateId, deadCount, deadIncr, highDangerCount, " \
                "midDangerCount, suspectedCount, suspectedCountIncr) " \
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.executemany(insertSql, dataList)
        con.commit()
        time.sleep(1.0)
        print(f"{time.asctime()}  保存国内总体疫情数据成功！")
        print(f"{time.asctime()}  共保存数据：" + str(idChina-1) + " 条")
        print()
    except:
        time.sleep(1.0)
        print(f"{time.asctime()}  保存国内总体疫情数据失败！正在进行回滚操作...")
        con.rollback()
        print()
    # 关闭连接
    cursor.close()
    con.close()


# 程序入口
if __name__ == '__main__':
    importWorldData()
    importWorldTotalData()
    importChinaData()
    importChinaTotalData()
