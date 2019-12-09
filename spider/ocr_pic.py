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


def save_pic(path, img):       
   
    with open(path, 'wb') as f:        
        f.write(img)


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files    
  
def ocr_pic():
       
    s = Session()
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token'
    header = {'Content-Type': 'application/json; charset=UTF-8'}

    #yh
    #data = {'grant_type': 'client_credentials',
    #'client_id': '***', # API key
    #'client_secret': '***' # Secret Key
    #}
    
    #cs1
    #data = {'grant_type':'client_credentials',    
    #'client_id': '***',
    #'client_secret': '***'
    #}
    
    #cs2
    data = {'grant_type':'client_credentials',    
    'client_id': '***',
    'client_secret': '***'
    }
    
    p = s.post(host, headers=header,data=data)
    js = json.loads(p.text)
    access_token = js['access_token']
    #url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token # 通用版地址
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token # 高精度版地址
    
    
    train_path = r'C:\Users\***\Desktop\yzm\train_pic'
    pic_list = file_name(train_path)
    
    for each in pic_list[:]:
        # # 二进制方式打开图文件
        #print(train_path+"\\"+each)
        train_pic = train_path+"\\"+each
        f = open(train_pic, 'rb') # 打开图片文件，需要指定文件名字
        # 参数image：图像base64编码
        img = base64.b64encode(f.read())
        f.close()
        params = {"image": img}
        header2 = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        pocr = s.post(url, headers=header, data=params)
        # print(pocr.text)
        js = json.loads(pocr.text)
        #print(js)
        if "error_code" not in js:
            for words in js["words_result"]:
                yzm_num = words['words'].replace(">", "")
                print(yzm_num)
    
            imgdata = base64.b64decode(img)
            test_path = r'C:\Users\***\Desktop\yzm\test_pic\{0}.jpg'.format(yzm_num)
            save_pic(test_path, imgdata)
            os.remove(train_pic)
            time.sleep(random.randint(1, 2))
    
    #return #words['words']


def ocr_table():
    
    s = Session()
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token'
    header = {'Content-Type':'application/json; charset=UTF-8'}
    data = {'grant_type':'client_credentials',
    'client_id':'***', # API key
    'client_secret':'***' # Secret Key
    }
    p = s.post(host, headers=header,data=data)
    js = json.loads(p.text)
    access_token = js['access_token']
    url = r'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request?access_token=' + access_token # 表格版地址
    url_re = r'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result?access_token=' + access_token
    
    o_path = r'C:\Users\***\Desktop\yzm'
    list = file_name(o_path)
    
    for each in list[:]:
        
        f = open(o_path+"\\"+each, 'rb') # 打开图片文件，需要指定文件名字
         # 参数image：图像base64编码
        img = base64.b64encode(f.read())
        params = {"image": img, "request_type": "excel"}
        header2 = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        pocr = s.post(url, headers=header2, data=params)
        # print(pocr.text)
        js = json.loads(pocr.text)
        print(js)
        
        time.sleep(40)
        request_id = js["result"][0]["request_id"]
        print(request_id)
        params2 = {"request_id": request_id, "request_type": "excel"}
        pocr_result = s.post(url_re, headers=header2, data=params2)
        js = json.loads(pocr_result.text)
        print(js)
        
        
def get_yzm_pic(name):
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
           "Cookie": "***"
    }    
    
    url = r"http://www.qhcourt.gov.cn:8080/wsfy-ww/cpws_yzm.jpg?n=0"
    pic = requests.get(url, headers=headers).content
    #path = r"C:\Users\***\Desktop\yzm\{0}.jpg".format(name)
    path = r"C:\Users\***\Desktop\pytorch-captcha-recognition-master\dataset\test\{0}.jpg".format(name)
    save_pic(path, pic)
    print(name) 
    
    

if __name__ == '__main__':
    
    #ocr_pic()
