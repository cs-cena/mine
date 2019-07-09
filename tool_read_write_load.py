#tool read,write,load,clean_word
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


def clean_word(text):
    new = []
    for i in text:
        new.append(i.replace(" ","").replace("\n","").replace("\t","").replace("\r",""))
    
    return new 
 

def read_csv(path):
    
    with open(path, "r", encoding="utf-8", newline='') as f:
        
        read = csv.reader(f)       
        rows = []
        
        for row in read:            
            rows.append(row)
    print("导入完成")
            
    return rows
   
    
def load_page(url, data, headers):

    response = requests.post(url, headers=headers, data=data)#,verify = False)

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text 

    
def load_page2(url, headers):

    response = requests.post(url, headers=headers)#,verify = False

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text
    
    
def load_page3(url, headers):

    response = requests.get(url, headers=headers, verify=False)#

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text

    
def load_page4(url, headers):

    response = requests.get(url, headers=headers, verify=False)#

    text = response.content.decode("gbk", 'ignore')

    #print(text)
    return text    
    
    
def load_page_prox(url, data, headers, proxies):#, proxies

    response = requests.post(url, headers=headers, data=data, proxies=proxies)# , verify = False, proxies=proxies,

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text 

#proxies = {'http': '47.112.80.214:8118'}    


def read_json():

    today = datetime.date.today()
    
    with open(r"C:\Users\***\Desktop\%s_%s"%(today, file_name), "r", encoding="utf-8") as f:

        data = json.load(f)    
        #load是从文件里面load,loads是从str里面load

        
def write_json(file_name,data):    

    today = datetime.date.today() 
    with open(r"C:\Users\***\Desktop\%_%s.json"%(today, file_name), "a", encoding="utf-8") as f:
        
        f.write(json.dumps(data,ensure_ascii=False,indent=4)) 
        
    
def write_csv(pt_name, rows):
    
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
