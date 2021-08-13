#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: test.py
@time: 2021/3/13 22:53
@software: PyCharm 2020.1.2(Professional Edition)
'''

import random


def generate_code(len=6):
    ''' 随机生成6位的验证码 '''
    # 生成的是0-9A-Za-z的列表
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        code_list.append(chr(i))
    print(code_list)
    str1 = random.sample(code_list, len)  # 从list中随机获取6个元素，作为一个片断返回
    print(str1)
    code = ''.join(str1)  # list to
    print(code)

generate_code()