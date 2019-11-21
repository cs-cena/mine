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
import qinghai_captcha_test

s = requests.session()

def load_page(url, data, headers):

    response = s.post(url, headers=headers, data=data)# , verify = False

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text
    
    
def load_page3(url, headers):

    response = s.get(url, headers=headers)#, verify=False

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
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
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
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }    
    
    url = r"http://www.qhcourt.gov.cn:8080/wsfy-ww/cpws_yzm.jpg?n=0"
    pic = s.get(url, headers=headers).content
    path = r"C:\Users\***\Desktop\pytorch-captcha-recognition-master\dataset\test\{0}.jpg".format(1)
    save_pic(path, pic)
    #print("pic done")
    

def get_yzm_num():   
    yzm = qinghai_captcha_test.main()
    return yzm

    
def write_txt(file_name, content):

    today = datetime.date.today() 
    
    with open(r"C:\Users\***\Desktop\%s_%s.txt"%(file_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        f.write(content)
        
        
def main():
    
    #每页需要新验证码
    erro_page = []

    for page in range(7, 8):
        
        #保存验证码图片
        get_yzm_pic()
        
        #识别验证码数字
        yzm_num = get_yzm_num()
        print(yzm_num)
        
        #post验证        
        isy = isyzm(yzm_num)
        print(isy)
        if "验证码错误" not in isy:
            
            headers = {
                   "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
            }
                    
            url = r"http://www.qhcourt.gov.cn:8080/wsfy-ww/fymh/3900/zxgk.htm?bzxrmc=&sxlx=&zjhm=&bzxrlx=&page={0}&yzm={1}".format(page, yzm_num)
            
            rq = load_page3(url, headers)
            
            if "未结执行实施案件" in rq:

                selector = etree.HTML(rq)
                
                #姓名
                aa = selector.xpath(r"//td[@class='td_data_row '][1]/div[@class='td_cell']/text()")
                
                #案件号
                bb = selector.xpath(r"//td[@class='td_data_row '][2]/div[@class='td_cell']/text()")
                #print(bb)
                
                #证件号码
                cc = selector.xpath(r"//td[@class='td_data_row '][3]/div[@class='td_cell']/text()")

                pages = [page]*len(aa)
                
                print(page)
                
                rows = []
                
                for item in list(zip(aa, cc, bb, pages)):
                    rows.append(item)
                
                write("qinghai", rows)
                time.sleep(random.randint(1, 2))
                
        elif "验证码错误" in isy:
            erro_page.append(page)
        
    print(erro_page)        

            
            
if __name__ == '__main__':
    
    main()
    
        
