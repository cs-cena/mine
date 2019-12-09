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
from PIL import Image
from selenium import webdriver


def read_csv(path):
    
    with open(path, "r", encoding="utf-8", newline='') as f:
        
        read = csv.reader(f)       
        rows = []
        
        for row in read:          
            rows.append(row[0])#不加[0]则是添加单个列表元素如[""]
    
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
  
    
#北京互金协会逃废债公示名单    
#在网页上抓这个url，看responce拉到最后可以看总数
def beijing():    
    
    url = "https://www.bjp2p.com.cn/malice/queryMaliceList"   

    headers = {#带cookie
    }              

    data = {     
        "name": "",
        "idcardno": "",
        "isLoss": "",
        "province": "",
        "hasCollection": "",
        "page": "1",
        "num": "207361"#207361 #192715 #191297
    }
    
    
    proxies = {'http': '124.205.155.154:9090'}
    
    response = load_page_prox(url, data, headers, proxies)#, proxies
    rq = json.loads(response)
    
    
    rows = [
                [
                "姓名或企业名称","身份证号或统一社会信用编码",
                "手机号码","区域/城市",
                "借款平台名称（简称）","累计借款金额（元）",
                "逾期金额（元）","逾期开始时间",
                "是否失联","催收情况"
                ]
              ]
                
    for item in rq["maliceList"]:
        
        row = [
            item["name"].replace(" ",""),
            item["idcardno"],
            item["phoneNo"],
            item["province"],
            item["platFormName"],
            item["totalLoanAmount"],
            item["overdue"],
            item["beginOverdueTime"].rstrip("\t"),
            item["isLoss"],
            item["hasCollectionDesc"]
        ]
            
        rows.append(row)
    
    write("bj", rows)
    print("complete")


def wulai():
    
    headers = {
    }
    
    for page in range(1, 7):
        
        print(page)
        
        url = r"http://www.credit-manage.com/app/breakRecords.htm?num=2&page={0}".format(page)
        
        res = json.loads(load_page2(url, headers))
                        
        list_wl = []
                    
        for ii in res["data"]:
            
            ct = ii["createTime"] / 1000
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ct))
            
            row = [
                ii["blackUserId"],
                ii["name"],
                ii["phone"],
                str(ii["certificateNo"]),
                ii["headPic"],
                ii["sex"],
                ii["age"],
                ii["homeAddress"],
                ii["province"],
                ii["city"],
                ii["district"],
                ii["createTime"],
                dt,
                ii["isExamine"],
                ii["sortAddress"],
                ii["isInclude"],
                ii["id"]
            ]
                
            list_wl.append(row)
        
        write("wl",list_wl)
        time.sleep(random.randint(1, 2))
         

def selenium_get_cookie():
    
    #from selenium import webdriver
    
    #设置为无界面
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    
    url = r"http://www.hshfy.sh.cn/shfy/gweb2017/channel_zx_list.jsp?pa=aemw9emJncwPdcssPdcssz"
    driver.get(url)
    
    td = driver.get_cookie("td_cookie")
    t = td["value"]
    
    jsid = driver.get_cookie("JSESSIONID")
    j = jsid["value"]
        
    #关闭窗口 关闭流浪器
    driver.close()
    driver.quit()
    
    return t, j


#应用 html.count("")
def qinghai_shixin():

    headers = {
    }
    
    for page in range(1, 231):#231
    
        print(page)
        url = r"http://112.126.102.76/exposure_item?p={0}&t=court".format(page)
        
        html = load_page3(url, headers)
        count_num = html.count('class="col-md-4"')
        #print(count_num)
    
        selector = etree.HTML(html)
        
        rows = []
        for num in range(1, count_num):
            cc = selector.xpath("//section[@class='row']/dl[@class='col-md-4'][{0}]/a[@class='exposure_item']/div[@class='clearfix']/dd/text()".format(num))
        
            if (len(cc[1]) <=4) :
                rows.append(cc)
        #print(rows)
        
        write("qinhai", rows)      


if __name__ == '__main__':
      
    #beijing()    
    #ningbo_xinyong()
