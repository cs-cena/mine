# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 20:33:05 2020

@author: Administrator
"""

import tushare as ts
import pandas as pd
import arrow
import time

ts.set_token('eef007250756de128a5b3b57ced98f74233335f880b300bfdafed700')
pro = ts.pro_api()


#获取一整年的日期
def isLeapYear(years):

    # 断言：年份不为整数时，抛出异常。
    assert isinstance(years, int), "请输入整数年，如 2018"
 
    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        # print(years, "是闰年")
        days_sum = 366
        return days_sum
    else:
        # print(years, '不是闰年')
        days_sum = 365
        return days_sum
 
 
def getDaysPerYear(years):

    start_date = '%s-1-1' % years
    a = 0
    date_list = []
    days_sum = 57 #控制天数 此isLeapYear(int(years)) 函数可获取全年天数

    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYYMMDD")
        a += 1
        date_list.append(b)
        
    return date_list


if __name__ == '__main__':

	#调用函数 获取指定天数
	#date_list = (i for i in getDaysPerYear("2020"))

	#单独天数更新
	date_list = ["20200301"]
	#print(date_list)

	for d in date_list:
	    df = pro.cctv_news(date=d)
	    df.to_csv(r'C:\Users\Administrator\Desktop\cctvNews\cctvNews_update.csv',mode='a',index=None, header=None)
	    #time.sleep(13)
	    