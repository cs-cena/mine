import requests
from lxml import etree
import re
import datetime
import time
import random
import json
import csv
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool


def load_page(url, data, headers):

    response = requests.post(url, headers=headers, data=data)# , verify = False

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text 
    
    
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\****\Desktop\shandong\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows) 
        
#先在index上找到内容链接"/sdfy_search/bzxr/findXzbzxInfos.do?bzxr.court_no=0F44"
#点进去再加载一页，找到http://www.sdcourt.gov.cn/sdfy_search/bzxr/xzbzxList.do，这就是需要post的        
def shandong_court(page):
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }    
        
    print(page)
    
    data = {
        "lx": "5",
        "bzxr.court_no": "0F",
        "bxzrmc": "",
        "curPage": page
    }
    
    #取pid的值
    url = r"http://www.sdcourt.gov.cn/sdfy_search/bzxr/xzbzxList.do"
    
    html = load_page(url, data, headers)
    
    #print(html)

    selector = etree.HTML(html)
    
    aa = selector.xpath(r"/html/body//td//input/@onclick")
    
    rows = []
    
    for i in aa:
        if "loadInfo" in i:
            index1 = i.find("(") + 2
            index2 = i.find(")") - 1
            pid = i[index1:index2]
            #pids.append([pid, page])
    
            #拿pid的值去匹内容
            url2 = r"http://www.sdcourt.gov.cn/sdfy_search/bzxrj/findxzgxfDetail.do"
            
            data2 = {
                "pid": pid,
                "lx": "5"
            }
            
            rq = json.loads(load_page(url2, data2, headers))
            
            cc = rq["bzxrDetail"]["bxzrmc"] #姓名
            dd = rq["bzxrDetail"]["zjhm"] #证件号码
            ee = rq["bzxrDetail"]["flwswh"] #案件号
            ff = rq["bzxrDetail"]["yzxfy"] #判决法院
            gg = rq["bzxrDetail"]["updateDate"]#公布时间
            
            row = [cc, dd, ee, ff, gg, pid, page]

            rows.append(row)
    
    write("shandong_court", rows)
    time.sleep(random.randint(0, 1))
        
        
if __name__ == '__main__':
    
    pool = ThreadPool()
    
    #page = (x for x in range(42470, 44148)) #44148
    
    try:
        start = time.time()
        
        for page in range(42501, 44148):
            pool.apply_async(shandong_court, [page])
        
        print('总耗时：%.5f秒' % float(time.time()-start))
       
    except Exception as e:
        
        print(str(e))
            
    pool.close()
    pool.join()    
