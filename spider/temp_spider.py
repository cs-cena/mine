import requests
from lxml import etree
import re
import datetime
import time
import random
import json
import csv
import pandas as pd
import multiprocessing
from pyquery import PyQuery as pq
import execjs
from io import BytesIO
from PIL import Image
from selenium import webdriver


def read_csv(path):
    
    with open(path, "r", encoding="utf-8", newline='') as f:
        
        read = csv.reader(f)       
        rows = []
        
        for row in read:          
            rows.append(row)
    
    print("导入完成")
            
    return rows
    
    
def read_2_csv(path):
    
    with open(path, "r", encoding="utf-8", newline='') as f:
        
        read = csv.reader(f)       
        rows = []
        
        for row in read:            
            rows.append(row)
            
    print("导入完成")
            
    return rows
   

def read_json():

    with open(r"C:\Users\***\Desktop\%s.txt"%n,"r",encoding="utf-8-sig") as f:            
        read = json.load(f)
        #load是从文件里面load,loads是从str里面load
    return read


def load_page_prox(url, data, headers, proxies):#, proxies

    response = requests.post(url, headers=headers, data=data, proxies=proxies)# , verify = False, proxies=proxies,

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text 

#proxies = {'http': '47.112.80.214:8118'}

def load_page(url, data, headers):

    response = requests.post(url, headers=headers, data=data)# , verify = False

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text
    
    
def load_page_gbk(url, data, headers):

    response = requests.post(url, headers=headers, data=data)# , verify = False

    text = response.content.decode("gbk", 'ignore')

    #print(text)
    return text   
    
    
def load_page2(url, headers):

    response = requests.post(url, headers=headers)#,verify = False

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text
    
    
def load_page3(url, headers):

    response = requests.get(url, headers=headers)#, verify=False

    text = response.content.decode("utf-8", 'ignore')#utf-8

    #print(text)
    return text

    
def load_page4(url, headers):

    response = requests.get(url, headers=headers)#, verify=False

    text = response.content.decode("gbk", 'ignore')

    #print(text)
    return text    
    
    
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\***\Desktop\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows)
        
        
def write_txt(file_name, content):

    today = datetime.date.today()
    
    with open(r"C:\Users\***\Desktop\%s_%s.txt"%(file_name, today), "a",
                  encoding="utf-8-sig", newline='') as f:
        
        f.write(content)


def clean_word(text):
    new = [i.replace(" ","").replace("\n","").replace("\r","") for i in text]
    return new


def temp():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }

    #data = {}

    for page in range(1, 2):

        print(page)

        url = r""
        
        html = load_page3(url, headers)
        #html = load_page(url, data, headers)
        #print(html)

        selector = etree.HTML(html)
        
        aa = selector.xpath()

        #页数
        #pages = [page]*len(aa)

        rows = []

        #for item in :
        #for item in list(zip()):
            #row = []
            #rows.append(row)
        
        #write("", rows)
        #time.sleep(random.randint(0, 1))


def temp_json():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }

    #data = {}

    url = ""

    #for page in range(1, 2):
    rp = json.loads(load_page(url, data, headers))
    #rq = json.loads(load_page3(url, headers))

    rows = []
        
    #for item in :
        #row = []
        #rows.append(row)

    #write("", rows)
    #time.sleep(random.randint(0, 1))

def temp_prox():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }

    #data = {}

    url = ""    

    proxies = {'http': '124.205.155.154:9090'} #ex

    response = load_page_prox(url, data, headers, proxies)#, proxies
    rq = json.loads(response)

    rows = []

    #for item in :
        #row = []
        #rows.append(row)

    #write("", rows)
    #time.sleep(random.randint(0, 1))

def temp_pd_readHtml():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }

    urls = [
            
    ]
    
    ff = []
    for url in urls[0:1]:
        html = load_page3(url, headers)
        data=pd.read_html(html, header=None, encoding='utf-8')
        df = data[0]#.iloc[2:, :]
        print(df)
        ff.append(df)
    #p = pd.concat(ff)
    #p.to_csv("C:/Users/***/Desktop/1.csv", mode='a', encoding='utf-8-sig', index=None, header=None)
    
    
def selenium_temp():
    
    from selenium import webdriver
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    urls = [
        r"",
    ]
    
    for url in urls:
        driver.get(url)
        time.sleep(random.randint(2, 3))
        xuhao = driver.find_elements_by_xpath(".//table[1]/tbody/tr/td[1]")
        
        rows = []
        for num in range(2, len(xuhao)):
            sfz = driver.find_elements_by_xpath(".//table[1]/tbody/tr[{}]/td".format(num))
            sfzs = [i.text for i in sfz]
            rows.append(sfzs)
            print(sfzs)
            
        
        write("", rows)
        #如果当前窗口关闭，则无法保持session
        #一个脚本的运行过程中，只打开一个webdriver浏览器即可
        #driver.close()
