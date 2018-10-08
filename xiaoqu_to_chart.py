#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
import webbrowser

import pandas as pd
import numpy as np
from pyecharts import Bar
import webbrowser as web
import os
import time
from lib.utility.version import PYTHON_3

if __name__ == '__main__':
    try:
        if PYTHON_3:
            os.system("ps aux | grep python | grep http.server | grep -v grep | awk '{print $2}' | xargs kill")
            os.system("python -m http.server 8080 & > /dev/null 2>&1 ")
        else:
            os.system("ps aux | grep python | grep SimpleHTTPServer | grep -v grep | awk '{print $2}' | xargs kill")
            os.system("python -m SimpleHTTPServer 8080 & > /dev/null 2>&1 ")
    except Exception as e:
        pass

    # 注意，已经将分割符号转换成分号，因为有的小区名中有逗号
    df = pd.read_csv("xiaoqu.csv", encoding="utf-8", sep=";")

    # 打印总行数
    print("row number is {0}".format(len(df.index)))

    # 过滤房价为0的无效数据
    df = df[df.price > 0]
    # # 去除重复行
    # df = df.drop_duplicates()
    print("row number is {0}".format(len(df.index)))

    df.sort_values("price", ascending=False, inplace=True)
    num = 3
    print(df.head(num))
    city = df["city_ch"][0]
    xqs = df["xiaoqu"][0:num]
    prices = df["price"][0:num]
    bar = Bar("{0}小区均价".format(city))
    bar.add("小区均价前{0}名".format(num), xqs, prices, is_stack=True, is_label_show=True)
    bar.render(path="xiaoqu.html")

    district_df = df.groupby('district').mean()
    print(district_df)
    districts = district_df.index
    prices = district_df["price"]
    bar = Bar("{0}区县均价".format(city))
    bar.add("区县均价排名", districts, prices, is_stack=True, is_label_show=True)
    bar.render(path="district.html")

    web.open("http://localhost:8080/xiaoqu.html", new=0, autoraise=True)
    web.open("http://localhost:8080/district.html", new=0, autoraise=True)
    # 确保页面打开
    time.sleep(15)

