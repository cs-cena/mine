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


def read_csv(path):
    with open(path, "r", encoding="utf-8", newline='') as f:
        read = csv.reader(f)
        rows = []
        for row in read:
            rows.append(row[6])
        print("导入完成")
    return rows     
    
    
def load_page3(url, headers):

    response = requests.get(url, headers=headers, verify=False)#

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text
   
    
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\***\Desktop\%s_%s.csv" % (pt_name, today), "a", encoding= "utf-8-sig", newline='') as f:
        writer = csv.writer(f) 
        writer.writerows(rows)
        
        
#卡农撞链接
def isempty(text):
    
    if text == []:
        text = [""]
    else:
        text = [text[0].replace(" ", "").replace("\n", "").replace("\r", "")]
    return text
        
    
 #卡农撞链接       
def kanong(page):
    
    headers_kn = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
                Chrome/17.0.963.56 Safari/535.11","Cookie":"kanong_6ab6_connect_is_bind=1; kanong_6ab6_smile=1D1; kanong_6ab6_nofavfid=1; kanong_6ab6_saltkey=tstyzCll; kanong_6ab6_lastvisit=1552870280; kanong_6ab6_atarget=1; kanong_6ab6_lastcheckfeed=146230%7C1554796652; kanong_6ab6_ulastactivity=1554805109%7C0; kanong_6ab6_forum_lastvisit=D_140_1554891504D_119_1554892202; kanong_6ab6_kn_unique=j75b3MX7PSXXS3R3vVz35pR335rmMs4v; Hm_lvt_9b95fb0ffb849e12ddf8136e9082a3fc=1554796435,1554889970,1554892207,1554960063; kanong_6ab6_visitedfid=140D119D198; kanong_6ab6_st_p=0%7C1554972653%7Cc66f29cb1aebb461daa5485449d6cbac; kanong_6ab6_viewid=tid_2151845; kanong_6ab6_lastact=1554972658%09plugin.php%09; Hm_lpvt_9b95fb0ffb849e12ddf8136e9082a3fc=1554972710; PHPSESSID=om20ue8p3eo9o6huolakrcfsbq; Hm_lvt_3c9700289866ebe56444d627bbcc7104=1552873987,1553767178,1554892259,1554974562; Hm_lpvt_3c9700289866ebe56444d627bbcc7104=1554975167"}
    
    #list_kn = ["贷款名称","期限","额度","费用","申请人数","上线时间","href"]
    #write("kanong",[list_kn])
    
    #https://daikuan.51kanong.com/
    url_kn = r"https://d.kanong.com/%s"%page    
    rq_kn = load_page3(url_kn, headers_kn)
    #print(rq_kn)
    print(page)
    
    if "老哥必做" not in rq_kn:
        
        selector = etree.HTML(rq_kn)
        ee = selector.xpath("//h2[@class='dk-top-tit']/text()")
        name = isempty(ee)

        aa = selector.xpath("//ul[@class='list-top cf']/li[2]/p[@class='red']/text()")
        term = isempty(aa)
        
        bb = selector.xpath("//ul[@class='list-top cf']/li[1]/p[@class='red']/text()")
        amount = isempty(bb)
        
        cc = selector.xpath("//ul[@class='list-top cf']/li[3]/p[@class='red']/text()")
        cost = isempty(cc)
        
        dd = selector.xpath("//ul[@class='list-top cf']/li[4]/p[@class='red']/text()")
        people = isempty(dd)
        
        ee = selector.xpath("//img[@class='dk-img']/@src")
        
        if len(ee[0]) < 7 :
            online_time = ["null"]
        else:
            e = ee[0].find("/20")+1               
            online_time = [ee[0][e:e+10]]
        
        row  = [
            name[0],
            term[0],
            amount[0],
            cost[0],
            people[0],
            online_time[0],
            page
        ]
            
        print(page)
        print(row)
        
        write("kanong", [row]) 
    
    if page%100 == 0: 
        time.sleep(5)

                        
if __name__ == '__main__':
    
    #步长
    #gap = 10000
    
    #page_list = [[x*gap,(gap+1)+x*gap] for x in range(0,3)]
      
    pool = ThreadPool()
    
    page = (x for x in range(1, 90001))#
    
    try:
        start = time.time()
        
        pool.map(kanong, page)
        
        print('总耗时step_href：%.5f秒' % float(time.time()-start))
       
    except Exception as e:
        
        print(str(e))
            
    pool.close()
    pool.join()
    
    #for i in range(1,100):
        #kanong(i)
