# -*- coding: UTF-8 -*-
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir+'/..')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import MultipleLocator
import numpy
from data import contract
import datetime

def main():
    month1 = input("please input month1 01 ~ 12:  ");
    month2 = input("please input month2 01 ~ 12:  ");

    cs = [
        ["jd14","gray"],
        ["jd15","pink"],
        ["jd16","green"],
        ["jd17","brown"],
        ["jd18","blue"],
        ["jd19","red"],
        ["jd20","black"]
    ]

    l = []
    name_list = []
    for i, val in enumerate(cs):
        a = val[0] + month1
        b = val[0] + month2
        if month2 < month1:
            if i >= len(cs)-1:
                continue
            b = cs[i+1][0]+month2
        l.append([a,b,a+" - "+b])
        name_list.append(a)
        name_list.append(b)
    
    datas = contract.load()
    m = contract.filter1(datas,name_list,False)

    ax = plt.gca()
    #指定X轴的以日期格式（带小时）显示
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    #X轴的间隔为小时
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    y_major_locator=MultipleLocator(100)
    ax.yaxis.set_major_locator(y_major_locator)

    diff_l = []
    for pair in l:
        diff_x = []
        diff_y = []
        if pair[0] not in m or pair[1] not in m:
            continue
        ma = m[pair[0]]
        mb = m[pair[1]]
        year = int("20"+pair[0][2:4])
        for (date,v) in ma.items():
            if date not in mb:
                continue
            diff_y.append(v - mb[date])
            print(2019 + date.year - year,date.month,date.day)
            diff_x.append(datetime.date(2019 + date.year - year,date.month,date.day))
                

        diff_l.append([pair[2],diff_x,diff_y])
        
    plt.xlabel("jd price diff " + month1 + " " + month2)
    plt.ylabel("")
    ls = []
    labels = []
    for i,v in enumerate(diff_l):
        plt.plot(v[1],v[2],color=cs[i][1],linestyle='-',linewidth = 1,label=v[0])
        labels.append(v[0])
    
    plt.legend(labels = labels,loc = 'best',shadow = True)
    plt.grid(axis="y",linestyle="--")
    plt.show()

main()