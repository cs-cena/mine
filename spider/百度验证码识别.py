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
import pandas as pd


def load_page3(url, headers):

    response = requests.get(url, headers=headers)#, verify=False

    text = response.content.decode("utf-8", 'ignore')#utf-8

    #print(text)
    return text

    
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\****\Desktop\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows)


def isyzm(num):
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
           "Cookie": ***
    }
        
    #74785 38369 47523
    data = {
        "tpyzm": num
    }
    
    url = r"http://www.qhcourt.gov.cn:8080/wsfy-ww/cpws/checkTpyzm.htm"
    rq = json.loads(load_page(url, data, headers))
    
    return rq
    
    
def save_pic(path, img):       
   
    with open(path, 'wb') as f:        
        f.write(img)
        
        
def get_yzm_pic():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
           "Cookie": ***
    }    
    
    url = r"http://www.qhcourt.gov.cn:8080/wsfy-ww/cpws_yzm.jpg?n=1"
    pic = requests.get(url, headers=headers).content
    path = r"C:\Users\****\Desktop\yzm\{0}.jpg".format(1)
    save_pic(path, pic)
    #print("pic done")
    

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
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token # 通用版地址
    #url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token # 高精度版地址
    
    
    o_path = r'C:\Users\****\Desktop\yzm'
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
            yyy = words['words']
    
    return yyy


def write_txt(file_name, content):

    today = datetime.date.today()
    
    with open(r"C:\Users\****\Desktop\%s_%s.txt"%(file_name, today), "a",
                  encoding="utf-8-sig", newline='') as f:
        
        f.write(content)
        
def main():
    
    #每页需要新验证码
    erro_page = []

    for page in range(25, 80):
        
        #保存验证码图片
        get_yzm_pic()
        
        #识别验证码数字
        yzm_num = get_yzm_num()
        
        #post验证        
        isy = isyzm(yzm_num)
        
        if "验证码错误" not in isy:
            
            print(page)
        
            headers = {
                   "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
                   "Cookie": ****
            }
                    
            url = r"http://www.qhcourt.gov.cn:8080/wsfy-ww/fymh/3901/zxgk.htm?bzxrmc=&sxlx=&zjhm=&bzxrlx=&page={0}&yzm={1}".format(page, yzm_num)
            
            rq = load_page3(url, headers)
            
            if "未结执行实施案件" in rq:
                #write_txt("1", rq)
                selector = etree.HTML(rq)
                
                #姓名
                aa = selector.xpath(r"//td[@class='td_data_row '][1]/div[@class='td_cell']/text()")
                
                #案件号
                bb = selector.xpath(r"//td[@class='td_data_row '][2]/div[@class='td_cell']/text()")
                #print(bb)
                
                #证件号码
                cc = selector.xpath(r"//td[@class='td_data_row '][3]/div[@class='td_cell']/text()")
                
                pages = [page]*len(aa)
                
                rows = []
                
                for item in list(zip(aa, cc, bb, pages)):
                    rows.append(item)
                
                write("xining", rows)
                time.sleep(random.randint(1, 2))
                
        elif "验证码错误" in isy:
            erro_page.append(page)
        
    print(erro_page)            

            
            
if __name__ == '__main__':
    
    main()
    
        
