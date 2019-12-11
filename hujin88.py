import pandas as pd
import requests
from lxml import etree
import re
import datetime
import time
import random
from bs4 import BeautifulSoup

def get_p2p():
    url_list=[]
    for i in range(1,15):
        url="https://dp.nifa.org.cn/HomePage?method=getPublishedInfo&currentPage=%d"%i
        a=requests.get(url)
        b=a.text
        c=BeautifulSoup(b,'lxml')
        d=c.find_all(class_="detail-btn")
        for j in d:
            url_list.append("https://dp.nifa.org.cn"+j["href"])
        
    
    total_df=[]
    x = 0
    for url in url_list:
    
    #    url="https://dp.nifa.org.cn/HomePage?method=getTargetOrgInfo&sorganation=91110106582593423A"
        a=requests.get(url)
        b=a.text
        
        c=BeautifulSoup(b,'lxml')
        name=c.find(style="font-size:18px;").text
        d=c.find_all(class_="table left-table1")[0]
        e=d.find_all("td")
        date_name,date_list,date_list1,date_isdel=[],[],[],[]
        i = 2
        while i in range(2,len(e)):
            date_name.append(name)
            date_list.append(e[i].text.strip('\r').strip('\n').strip('\t').strip('\r\n'))
            date_list1.append(e[i+1].text.strip('\r').strip('\n').strip('\t').strip('\r\n'))
            if e[i]['class'][0]=="table-label" and (len(e[i]['class'])==1):
                date_isdel.append(0)
            else:
                date_isdel.append(1)
            i += 2
        temp_df=pd.DataFrame()
        temp_df["name"]=date_name
        temp_df["date"]=date_list
        temp_df["date1"] = date_list1
        temp_df["isdel"]=date_isdel
        
        d=c.find_all(class_="table right-table")[0]
        right=str(d)
        data=pd.read_html(right,header=0,encoding='utf-8')   
         
        xx=pd.merge(temp_df,data[0],left_index=True,right_index=True)
        total_df.append(xx)
        
        x+=1
        print(x)
        
    p=pd.concat(total_df)
    p.to_csv("C:/Users/****/Desktop/p2p_191211.csv",encoding='utf-8-sig',index=None)
    
    
    left=str(d)
    date=pd.read_html(left,header=0,encoding='utf-8')
 
if __name__ == '__main__':
   
    get_p2p()
