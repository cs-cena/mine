import requests
from lxml import etree
import re
import datetime
import time
import random
import json
import csv
import base64, sys, ssl
from requests import Session
import os


def load_page3(url, headers):

    response = requests.get(url, headers=headers)#, verify=False

    text = response.content.decode("utf-8", 'ignore')#utf-8

    #print(text)
    return text

    
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\***\Desktop\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows)


def isyzm(num):
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
           "Cookie": "SESSION=480f7e01-232e-472e-80c7-4269b4631f98; TS01ecb577=01bec5b6b3e09ba3eeab2dafac543dfd4ad1de941c920892239da1e3a46593061416815acf8b9ce94f69cd1bd90f1734bf5b3ba12b; TS01e5d7ed=01bec5b6b336a0ad82915c9ff32cd61fea3771f700d246c6a5e9f93f71f1062092c1de0e08e529bcb6fb0ce48610e69c460e0e2a4c"
    }
        
    #74785 38369 47523
    data = {
        "tpyzm": num
    }
    
    url = r"http://www.xjcourt.gov.cn/susong51/cpws/checkTpyzm.htm"
    rq = json.loads(load_page(url, data, headers))
    print(rq)
    
    
def save_pic(path, img):       
   
    with open(path, 'wb') as f:        
        f.write(img)
        
        
def get_yzm_pic():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
           "Cookie": "SESSION=480f7e01-232e-472e-80c7-4269b4631f98; TS01ecb577=01bec5b6b3e09ba3eeab2dafac543dfd4ad1de941c920892239da1e3a46593061416815acf8b9ce94f69cd1bd90f1734bf5b3ba12b; TS01e5d7ed=01bec5b6b336a0ad82915c9ff32cd61fea3771f700d246c6a5e9f93f71f1062092c1de0e08e529bcb6fb0ce48610e69c460e0e2a4c"
    }    
    
    url = r"http://www.xjcourt.gov.cn/susong51/cpws_yzm.jpg?n=1"
    pic = requests.get(url, headers=headers).content
    path = r"C:\Users\chensheng\Desktop\yzm\{0}.jpg".format(1)
    save_pic(path, pic)
    print("pic done")
    

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files    
        
        
def get_yzm_num():
       
    s = Session()
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token'
    header = {'Content-Type':'application/json; charset=UTF-8'}
    data = {'grant_type':'client_credentials',
    'client_id':'OrBbPylC903GyGkjQgC88iUL', # API key
    'client_secret':'59lm2mvNb6xfl3Q1udiNGM6bOLoybfnT' # Secret Key
    }
    p = s.post(host, headers=header,data=data)
    js = json.loads(p.text)
    access_token = js['access_token']
    # url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token # 通用版地址
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token # 高精度版地址
    
    
    o_path = r'C:\Users\chensheng\Desktop\yzm'
    list = file_name(o_path)
    
    for each in list[:]:
        # # 二进制方式打开图文件
        #print(o_path+"\\"+each)
        f = open(o_path+"\\"+each, 'rb') # 打开图片文件，需要指定文件名字
        # 参数image：图像base64编码
        img = base64.b64encode(f.read())
        params = {"image": img}
        header2 = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        pocr = s.post(url,headers=header, data=params)
        # print(pocr.text)
        js = json.loads(pocr.text)
        for words in js["words_result"]:
            print(words['words'])
    
    return words['words']


def main():
    
    #每页需要新验证码
    for page in range(72, 77):  
        
        #保存验证码图片
        get_yzm_pic()
        
        #识别验证码数字
        yzm_num = get_yzm_num()
        
        #post验证
        isyzm(yzm_num)
        
        
        headers = {
               "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
               "Cookie": "SESSION=480f7e01-232e-472e-80c7-4269b4631f98; TS01ecb577=01bec5b6b3e09ba3eeab2dafac543dfd4ad1de941c920892239da1e3a46593061416815acf8b9ce94f69cd1bd90f1734bf5b3ba12b; TS01e5d7ed=01bec5b6b336a0ad82915c9ff32cd61fea3771f700d246c6a5e9f93f71f1062092c1de0e08e529bcb6fb0ce48610e69c460e0e2a4c"
        }
                
        url = r"http://www.xjcourt.gov.cn/susong51/fymh/4050/zxgk.htm?bzxrmc=&sxlx=&zjhm=&bzxrlx=&jbfy=&page={0}&yzm={1}".format(page, yzm_num)
        rq = load_page3(url, headers)
        
        if "未结执行实施案件" in rq:
            print("成功爬取")
    

if __name__ == '__main__':
    
    main()
