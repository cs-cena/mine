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
#融360 18114878104 qaz12345
#https://m.rong360.com/center


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

    response = requests.get(url, headers=headers, verify=False)#

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

        
def daima():
    '''
    #贷码 post带data 包含现金贷下属 每日更新 & 更多产品
    #http://daima.jsdgw.top/index/index/daedaikuan.html
    url_daima_xj = "http://daima.jsdgw.top/index/index/shou.html"  
    
    data_daimai = {"type": "1"}
   
    headers_daima = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
        "Cookie": "PHPSESSID=a1bifd5rji052cln1j15b8skr2"
    }
        
               
    rq_daima_xj = json.loads(load_page(url_daima_xj, data_daimai, headers_daima))
    
    list_daima = [["平台名字", "类型", "备注"]]
        
    for a in rq_daima_xj["data"]["xinpin"]:   
        
        #print(a["name"])
        an = a["name"].replace('1', '').replace('2', '') #平台名字里含1,2数字
        list_daima.append([an, "现金贷"])
   '''
   
    #贷码 post没有data 包含网贷下属 网贷推荐 & 全部网贷
    url_daima_wd = "http://daima.jsdgw.top/index/index/wangdai.html" 
       
    headers_daima = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
        "Cookie": "PHPSESSID=a1bifd5rji052cln1j15b8skr2"
    }
    
    rq_daima_wd = json.loads(load_page2(url_daima_wd, headers_daima))
    
    list_daima = [["平台名字", "类型", "备注"]]
    
    for b in rq_daima_wd["data"]["xinpin"]:
        
        bn = b["name"].replace('1', '').replace('2', '')        
        list_daima.append([bn, "网贷", b["beizhu"]])
    
    print(bn[1])
    
    write("daima", list_daima)
    #print("贷码 已完成")


#fiddler先点click to decode 不然乱码。保存entire response txt文件 去除报头
def r360():    
    #现金贷口子只在融360app上看得见，下融360手机app,用fiddler抓app数据包，数据都在这个url的返回里https://bigapp.rong360.com/taojinyun/productlist/taojinlist
    #但不能直接爬，有反爬机制，直接用fiddler保存数据为txt即可，下载后把里面的报头都删了，留下json。
    
    with open(r"C:\Users\***\Desktop\1.txt", encoding="utf-8-sig") as f:
        content = json.load(f)
        
    rows = [["产品名", "额度范围", "审核时间", "预估时间", "月费率", "贷款期限"]]
    
    for each in content["data"]["taojin_product_list"]:
        
        name = each["product_name"]

        try:
            amount = each["full_credit"]["crm_amount"]
        except:
            try:
                amount = each["loan_quota_str"]
            except:
                amount = ""
        #print(amount)
        
        try:
            loan_approve_time = each["loan_approve_time_str"]
        except:
            loan_approve_time = ""
        #print(loan_approve_time)
        
        try:
            loan_time = each["loan_fangkuan_shenpi_time_str"].replace('<font color="#999999">', '').replace('</font>', '')
        except:
            loan_time = ""
        #print(loan_time)
        
        try:
            if each["loan_rate_str2"]:
                ratio = each["loan_rate_str2"]
            elif each["loan_rate_str"]:
                ratio = each["loan_rate_str"]
        except:
            try:
                ratio = each["loan_rate_str"]
            except:
                ratio = ""
        #print(ratio)
        
        try:
            duration = each["loan_term_str"]
        except:
            #break
            duration = ""
        #print(duration)
        
        row = [name, amount, loan_approve_time, loan_time, ratio, duration]

        rows.append(row)
    
    write("r360", rows)
    
    print("r360 已完成")

    
def qianjie():
    
    url_qianjie = "https://jkzj-api.fqgj.net/qianjie/speed/company/list"

    headers_qianjie = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"} 
    
    data_qianjie = {
        "appKey": "17171",
        "appClient": "android",
        "versionCode": "20190115",
        "longitude": "121.63661193847656",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiL3VzZXIvbG9naW4iLCIxNTUxMTcwNDQ0Mjk5IiwiMjA4NTkyMTUiXX0.DbagFYCKFW2glL12GnWRwBM3iLXwFyaHDJg3OSACHng",
        "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOjE2LCJleHQiOjE1NTM3NjI0NDQyNzEsInVpZCI6IjE5MDIyNjk5MzIyMTM1NzgwMCIsImdzdCI6Ijg2MTg2ODAzNDQyNDE0MSIsImFjbCI6Mn0.GKkt_VRKDBwFzLCUuPxD2rPuTgJS2PwdVLuqIKvNzYA",
        "timestamp": "1551256677",
        "appSign": "8031d0eecda59cc5d437cf4b791f6d83",
        "net": "WIFI",
        "clientId": "13065ffa4e55e5b0b61",
        "appVersion": "1.4.0",
        "imei": "861868034424141",
        "coreVersion": "17",
        "mobileModel": "m1 metal",
        "ip": "27.115.63.90",
        "latitude": "31.226547241210938",
        "channel": "xandroid6000_x22",
        "cityId": "73",
        "params": {"pageSize":100, "pageNo":2, "orderId":0}
        }
    
    rp_qianjie = json.loads(load_page(url_qianjie, data_qianjie, headers_qianjie))
    
    list_qianjie = [["平台名字", "预估额度", "综合利率"]]
    
    for qj in rp_qianjie["data"]["speedCompanyList"]["records"]:
        
        name = qj["companyName"] #平台名字
        amount = qj["estimateAmount"] #预估额度
        rate = qj["complexRate"] #综合利率
        
        row = [name, amount, rate]

        list_qianjie.append(row)
    
    print(list_qianjie)

    
def youmi():   
    
    url_youmi = "http://api.ryingvip.com/service/index/loan?pageNum=1&pageSize=100&clientType=android&channel=ymgj&appVersion=1.0.4&deviceId=861868034424141&mobilePhone=18114878104&deviceName=m1%20metal&osVersion=5.1&appName=jsxjx&packageId=com.innext.ymgj&appMarket=ymgj-meizu&merchantNumber=cjxjx&userId=16050162&merchant=cjxjx&platform=1"
    
    headers_youmi = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"} 
    
    rp_youmi = json.loads(load_page2(url_youmi, headers_youmi))
    
    list_youmi = [["平台名字", "额度范围", "期限"]]    

    for y1 in rp_youmi["data"]["products1"]:   
        
        name1 = y1["productName"]
        amount1 = y1["amountRange"]
        time1 = y1["termInfo"]        
 
        row1 = [name1, amount1, time1]

        list_youmi.append(row1)
        
    for y2 in rp_youmi["data"]["products2"]["list"]:

        name2 = y2["productName"]
        amount2 = y2["amountRange"]
        time2 = y2["termInfo"]

        row2 = [name2, amount2, time2]

        list_youmi.append(row2)
            
    write("youmi", list_youmi)    

    
def dkgj():
    
    url_dkgj = "http://loan.mydkguanjia.com/loanCenter/productloan/list"

    headers_dkgj = {"User-Agent":"xulugj://4.12.0 (Android;android22;zh_CN;ID:2-821d204430d0413183f89e03519e9ca7-861868034424141-meizu-708d34db466325dd0b4fe0cb98667418)"}
    
    data_qianjie = {
        "appKey":"17171","appClient":"android",
        "versionCode":"20190115",
        "longitude":"121.63661193847656",
        "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiL3VzZXIvbG9naW4iLCIxNTUxMTcwNDQ0Mjk5IiwiMjA4NTkyMTUiXX0.DbagFYCKFW2glL12GnWRwBM3iLXwFyaHDJg3OSACHng",
        "accessToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOjE2LCJleHQiOjE1NTM3NjI0NDQyNzEsInVpZCI6IjE5MDIyNjk5MzIyMTM1NzgwMCIsImdzdCI6Ijg2MTg2ODAzNDQyNDE0MSIsImFjbCI6Mn0.GKkt_VRKDBwFzLCUuPxD2rPuTgJS2PwdVLuqIKvNzYA",
        "timestamp":"1551256677",
        "appSign":"8031d0eecda59cc5d437cf4b791f6d83",
        "net":"WIFI",
        "clientId":"13065ffa4e55e5b0b61",
        "appVersion":"1.4.0",
        "imei":"861868034424141",
        "coreVersion":"17",
        "mobileModel":"m1 metal",
        "ip":"27.115.63.90",
        "latitude":"31.226547241210938",
        "channel":"xandroid6000_x22",
        "cityId":"73",
        "params":{"pageSize":100,"pageNo":2,"orderId":0}
        }
    
    rp_qianjie = json.loads(load_page(url_qianjie, data_qianjie, headers_qianjie))
    
    list_qianjie = [["平台名字", "预估额度", "综合利率"]]
    
    for qj in rp_qianjie["data"]["speedCompanyList"]["records"]:
        
        name = qj["companyName"] #平台名字
        amount = qj["estimateAmount"] #预估额度
        rate = qj["complexRate"] #综合利率
        
        row = [name, amount, rate]

        list_qianjie.append(row)
    
    print(list_qianjie)
    
    
def koko():
    
    list_koko = [["平台名字", "额度", "期限", "删", "利率"]]
    
    for num in range(1000,2000):
        
        print(num)        
        
        url_koko = "http://kmjrapp.kokoqiandai.com/wap/applyl.php?u_id=15197&commodity=loan%s"%num
        
        headers_koko = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
            Chrome/17.0.963.56 Safari/535.11"}
            
        rq_koko = load_page3(url_koko,headers_koko)
    
        if '<p style="font-size:3rem">产品已下架！</p></div>' not in rq_koko:
            
            selector = etree.HTML(rq_koko)            
            content = selector.xpath("//div[1]/span[1]/text()")            
            rate = selector.xpath("//div[@class='loanqi'][1]/div[2]/span[1]/text()")
            
            content.extend(rate)
            
            list_koko.append(content)

    print(list_koko)
    
    write("koko", list_koko)
    

#fiddler直接保存entire response，去除报头。##内容拉到最后有0，注意删掉##
#https://static.huaqianwy.com/api/product/filter  有5个
def dkw2345():    
    
    #需拖动，有好几个，拉一次显示10个保存一次
    list_dkw = [["平台名字", "额度", "期限", "综合利率", "条件"]]
    
    for n in range(1,5):
        
        with open(r"C:\Users\***\Desktop\%s.txt"%n,"r",encoding="utf-8-sig") as f:            
            dkw_content = json.load(f)
            #load是从文件里面load,loads是从str里面load
        
        for item in dkw_content["body"]["page"]:
            
            row = [
                item["name"],
                item["limit"],
                item["duration"],
                item["rate"],
                item["applyTips"]
                ]
                
            list_dkw.append(row)
    
    write("2345dkw",list_dkw)
    
    
#fiddler直接保存entire response，去除报头。##内容拉到最后有0，注意删掉##
#http://gw.jiedianqian.com/gateway.do  
def jdqdk():    
    
    list_jdqdk = [["平台名字", "月利率", "期限(天)", "条件"]]
    
    #需拖动，有好几个，拉一次显示10个保存一次
    for n in range(1,5):
        
        with open(r"C:\Users\***\Desktop\%s.txt"%n,"r",encoding="utf-8-sig") as f:
            jdqdk_content = json.load(f)
            #load是从文件里面load,loads是从str里面load
           
        for item in jdqdk_content["data"]["allList"]:
            
            rate = "%s"%(item["month_fee_rate"]/100) + "%" #月利率 
            amount = "%s-%s"%(item["minTerms"], item["maxTerms"]) #按天
            
            row = [
                item["newProductName"],
                rate,
                amount,
                item["description"]
                ]
                
            list_jdqdk.append(row)
    
    write("jdqdk", list_jdqdk)
    
    
#fiddler直接保存
#https://beidou.geinihua.com/gnh-bdplatform-gt/api/v1/main/getHot
def geinihua():    
    
    list_geinihua = [["平台名字", "额度范围", "综合利率(月)"]]
    
    with open(r"C:\Users\***\Desktop\1.txt","r",encoding="utf-8-sig") as f:
        geinihua_content = json.load(f)
       #load是从文件里面load,loads是从str里面load
    
    for item in geinihua_content["businessObj"]["Config"]:
        
        row = [
            item["LoanName"],
            item["Money"],
            "{0}{1}".format(item["Score"],
            "%")
            ]
            
        list_geinihua.append(row)
    
    write("geinihua", list_geinihua)
   
    
#北京互金协会逃废债公示名单    
#在网页上抓这个url，看responce拉到最后可以看总数
def beijing():    
    
    url_bj = "https://www.bjp2p.com.cn/malice/queryMaliceList"   
    
    #headers_bj = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
                 # Chrome/17.0.963.56 Safari/535.11"}

    headers_bj = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Content-Length":"62",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":"td_cookie=3033775304; Hm_lvt_97f110905a34b097ed49b9e9a86c55da=1559182513,1559182595,1559182644,1559182723; JSESSIONID=3E6FD2F058A7752D0FF6A835BAD0605B; Hm_lpvt_97f110905a34b097ed49b9e9a86c55da=1559193681",
        "Host":"www.bjp2p.com.cn",
        "Origin":"https://www.bjp2p.com.cn",
        "Referer":"https://www.bjp2p.com.cn/malice/maliceList",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
    }              

    data_bj ={     
        "name": "",
        "idcardno": "",
        "isLoss": "",
        "province": "",
        "hasCollection": "",
        "page": "1",
        "num": "151428"
    }
    
    
    proxies = {'http': '124.205.155.154:9090'}
    
    response = load_page_prox(url_bj, data_bj, headers_bj, proxies)#, proxies
    rq_bj = json.loads(response)
    
    #with open(r'C:\Users\***\Desktop\bj.json', 'w', encoding='utf-8') as json_file:
        #json.dump(rq_bj, json_file, ensure_ascii=False)
        #print("write json file success!")
    
    list_bj = [
                [
                "姓名或企业名称","身份证号或统一社会信用编码",
                "手机号码","区域/城市",
                "借款平台名称（简称）","累计借款金额（元）",
                "逾期金额（元）","逾期开始时间",
                "是否失联","催收情况"
                ]
              ]
                
    for item in rq_bj["maliceList"]:
        
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
            
        list_bj.append(row)
    
    write("bj",list_bj)
    print("complete")

    
#网贷天眼已暴雷平台名单
#共270页，5385家暴雷平台
def wdty_blacklist():
    
    list_wdty = [["平台名字","问题发生时间","上线时间","所在地区","出问题原因"]]

    for num in range(1,271):
        
        url_wdty = "https://www.p2peye.com/platformData.php?mod=issue&ajax=1&action=getPage&page={0}".format(num)
        
        headers_wdty = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
        Chrome/17.0.963.56 Safari/535.11"}
        
        rq_wdty = json.loads(load_page2(url_wdty, headers_wdty))
        #print(rq_wdty)
        
        for item in rq_wdty["data"]:
            
            row = [
                item["name"],
                item["black_time"],
                item["online_time"],
                item["city_name"],
                item["black_type_name"]
                ]  
                
            list_wdty.append(row)
            
        print(num)
        
    write("wdty_blacklist",list_wdty)

#卡农超市 
'''   
def kanong_market():
   
    temp = [[], [], [], [], []]
    
    for ee in range(1,6):
        
        url_kn = r"https://daikuan.51kanong.com/Home/Daikuan/lists/class/%s.html"%str(ee)
        #url_kn = r"https://daikuan.51kanong.com/daikuan/lists/p/1"
        
        headers_kn = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
            Chrome/17.0.963.56 Safari/535.11","Cookie":"kanong_6ab6_connect_is_bind=1; kanong_6ab6_smile=1D1; kanong_6ab6_nofavfid=1; kanong_6ab6_saltkey=tstyzCll; kanong_6ab6_lastvisit=1552870280; kanong_6ab6_atarget=1; kanong_6ab6_lastcheckfeed=146230%7C1554796652; kanong_6ab6_ulastactivity=1554805109%7C0; kanong_6ab6_forum_lastvisit=D_140_1554891504D_119_1554892202; kanong_6ab6_kn_unique=j75b3MX7PSXXS3R3vVz35pR335rmMs4v; Hm_lvt_9b95fb0ffb849e12ddf8136e9082a3fc=1554796435,1554889970,1554892207,1554960063; kanong_6ab6_visitedfid=140D119D198; kanong_6ab6_st_p=0%7C1554972653%7Cc66f29cb1aebb461daa5485449d6cbac; kanong_6ab6_viewid=tid_2151845; kanong_6ab6_lastact=1554972658%09plugin.php%09; Hm_lpvt_9b95fb0ffb849e12ddf8136e9082a3fc=1554972710; PHPSESSID=om20ue8p3eo9o6huolakrcfsbq; Hm_lvt_3c9700289866ebe56444d627bbcc7104=1552873987,1553767178,1554892259,1554974562; Hm_lpvt_3c9700289866ebe56444d627bbcc7104=1554975167"}
            
        rq_kn = load_page3(url_kn,headers_kn)
        selector = etree.HTML(rq_kn)
                
        #贷款名称
        item_name = selector.xpath("//td[@class='logo']/span/text()")
        temp[0].extend(item_name)
        
        #贷款额度,产品描述,费用,申请人数
        for kw in ['prosition', 'info', 'cost', 'time']:
            dd = []
            
            for cc in range(1, len(item_name)+1):
                
                path = "//tr[@class='filter-tr'][{0}]/td[@class='{1}']/text()".format(cc, kw)
                item = selector.xpath(path)
                
                if item == []:
                    item = [""]
                    dd.append(item[0])
                else:
                    dd.append(item[0])
            
            if kw == 'prosition':
                temp[1].extend(dd)
            elif kw == 'info':
                temp[2].extend(dd)
            elif kw == 'cost':
                temp[3].extend(dd)
            else:
                temp[4].extend(dd)
                
        #查看是否列表元素个数
        for ss in temp:
            print(len(ss))
    
    data = {
        "贷款名称":temp[0],
        "贷款额度":temp[1],
        "产品描述":temp[2],
        "费用":temp[3],
        "申请人数":temp[4]
        }
        
    df = pd.DataFrame(data)
    
    print(df)    
    
    df.to_csv("C:/Users/***/Desktop/kanong.csv",encoding='utf-8-sig',index=None)    
'''     


#卡农撞链接
def isempty(text):
    
    if text == []:
        text = [""]
    else:
        text = [text[0].replace(" ","").replace("\n","").replace("\r","")]
    return text
        
    
 #卡农撞链接       
def kanong(begin, end, filenum):
    
    headers_kn = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
                Chrome/17.0.963.56 Safari/535.11","Cookie":"kanong_6ab6_connect_is_bind=1; kanong_6ab6_smile=1D1; kanong_6ab6_nofavfid=1; kanong_6ab6_saltkey=tstyzCll; kanong_6ab6_lastvisit=1552870280; kanong_6ab6_atarget=1; kanong_6ab6_lastcheckfeed=146230%7C1554796652; kanong_6ab6_ulastactivity=1554805109%7C0; kanong_6ab6_forum_lastvisit=D_140_1554891504D_119_1554892202; kanong_6ab6_kn_unique=j75b3MX7PSXXS3R3vVz35pR335rmMs4v; Hm_lvt_9b95fb0ffb849e12ddf8136e9082a3fc=1554796435,1554889970,1554892207,1554960063; kanong_6ab6_visitedfid=140D119D198; kanong_6ab6_st_p=0%7C1554972653%7Cc66f29cb1aebb461daa5485449d6cbac; kanong_6ab6_viewid=tid_2151845; kanong_6ab6_lastact=1554972658%09plugin.php%09; Hm_lpvt_9b95fb0ffb849e12ddf8136e9082a3fc=1554972710; PHPSESSID=om20ue8p3eo9o6huolakrcfsbq; Hm_lvt_3c9700289866ebe56444d627bbcc7104=1552873987,1553767178,1554892259,1554974562; Hm_lpvt_3c9700289866ebe56444d627bbcc7104=1554975167"}
    
    #list_kn = ["贷款名称","期限","额度","费用","申请人数","上线时间","href"]
    #write("kanong",[list_kn])
    
    for num in range(begin, end):#50001
    
        url_kn = r"https://daikuan.51kanong.com/%s"%num
        rq_kn = load_page3(url_kn, headers_kn)
        
        
        if "借款有风险，申请需谨慎" in rq_kn:
            
            selector = etree.HTML(rq_kn)
            ee = selector.xpath("//span[@class='product-name']/text()")
            item_name = isempty(ee)
    
            aa = selector.xpath("//div[@class='moreinfo']/table/tbody/tr[1]/td[3]/i/text()")
            item_term = isempty(aa)
            
            bb = selector.xpath("//div[@class='moreinfo']/table/tbody/tr[1]/td[2]/i/text()")
            item_amount = isempty(bb)
            
            cc = selector.xpath("//div[@class='moreinfo']/table/tbody/tr[2]/td[1]/i/text()")
            item_cost = isempty(cc)
            
            dd = selector.xpath("//div[@class='moreinfo']/table/tbody/tr[1]/td[1]/i/text()")
            item_people = isempty(dd)
            
            ee = selector.xpath("//div[@class='item']/img/@src")
            
            if len(ee[0]) < 7 :
                item_online_time = ["null"]
            else:
                e = ee[0].find("/20")+1               
                item_online_time = [ee[0][e:e+10]]
            
            row  = [
                item_name[0],
                item_term[0],
                item_amount[0],
                item_cost[0],
                item_people[0],
                item_online_time[0],
                num
                ]
                
            print(num)
            print(row)
            
            write("kanong_"+str(filenum),[row]) 
        
        if num%500 == 0: 
            time.sleep(10)

            
 #卡农撞链接，加进程           
def kanong_process():
        
    p1 = multiprocessing.Process(target = kanong, args = (1,20001,12))
    p2 = multiprocessing.Process(target = kanong, args = (20001,40001,24))
    p3 = multiprocessing.Process(target = kanong, args = (40001,60001,46))
    p4 = multiprocessing.Process(target = kanong, args = (60001,90001,69))
    
    
    print("子进程即将开始")
    start =time.clock()
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    end = time.clock()
    print("子进程完成")
    
    print("-"*50)
    print('运行时长: %s 秒'%(end-start))
    print("-"*50)              
            
            
def kashen():
    
    headers_ks = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
                Chrome/17.0.963.56 Safari/535.11"}                
        
    list_href = []
   
    for num in range(1,23):
        
        url_ks = r"https://www.kashen.com/dk_list_0_0_0_%s.html"%num
        rq_ks = load_page3(url_ks, headers_ks)
        #print(rq_ks) 
        selector1 = etree.HTML(rq_ks)
        item_href = selector1.xpath("//div[@class='deansubjectionslist']/ul/li/div[@class='deansubdetails']/h5/a/@href")
        #print(item_href)
        list_href.extend(item_href)    
        
    n = 0    
    
    list_ks_kouzi = [
                     [
                     "贷款名称","期限","额度",
                     "费用","征信要求","资料",
                     "类别","到账方式", "客服电话"
                     ]
                    ]
                     
    for href in list_href:
        
        url_ks_kouzi = r"https://www.kashen.com/%s"%href
        rq_ks_kouzi = load_page3(url_ks_kouzi, headers_ks)
        selector = etree.HTML(rq_ks_kouzi)
   
        item_name = selector.xpath("//span[@class='product-name']/text()")[0]
        
        aa = selector.xpath("//div[@class='moreinfo']/table/tbody/tr[1]/td[2]/i/text()")
        item_term = isempty(aa)        
        
        bb = selector.xpath("//div[@class='moreinfo']/table/tbody/tr[1]/td[1]/i/text()")
        item_amount = isempty(bb)
        
        cc = selector.xpath("//div[@class='moreinfo']/table/tbody/tr[1]/td[3]/i/text()")
        item_cost = isempty(cc)
        
        dd = selector.xpath("//div[@class='content']/table/tbody/tr[1]/td[1]/i/text()")
        item_zhengxin = isempty(dd)
        
        ee = selector.xpath("//div[@class='content']/table/tbody/tr[1]/td[2]/i/text()")
        item_ziliao = isempty(ee)
                
        ff = selector.xpath("//div[@class='content']/table/tbody/tr[1]/td[3]/i/text()")
        item_leibie = isempty(ff)
        
        gg = selector.xpath("//div[@class='content']/table/tbody/tr[2]/td[1]/i/text()")
        item_daozhang = isempty(gg) 
        
        hh = selector.xpath("//div[@class='content']/table/tbody/tr[2]/td[3]/i/text()")
        item_mobnum = isempty(hh)
                
        row = [
            item_name,item_term[0],
            item_amount[0],
            item_cost[0],
            item_zhengxin[0],
            item_ziliao[0],
            item_leibie[0],
            item_daozhang[0],
            item_mobnum[0]
            ]
            
        list_ks_kouzi.append(row)
        
        n+=1
        print(n)
        
    write("kashen", list_ks_kouzi) 
    
    
def zhongxin():
    
    headers_zx = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko)\
                Chrome/17.0.963.56 Safari/535.11"}                

    #one = ["贷款名称", "期限", "额度", "费用", "上线时间"]            
    #write("zhongxin", [one]) 
           
    for num in range(96,105):#105
    
        url_zx = r"https://www.zhongxinwanka.com/thread-htm-fid-95-page-%s.html"%num
        rq_zx = load_page4(url_zx, headers_zx)
        #print(rq_zx) 
        selector1 = etree.HTML(rq_zx)
        item_href = selector1.xpath("//form[@id='moderate']/li/div[@class='deansubdetails']/h5/a/@href")
        #94页有个自如口袋 没了 要把链接剔除thread-17842-1-1.html 删了以后单爬，然后跳过即可
        #item_href.remove("thread-17842-1-1.html")
        #print(item_href)
        
        n = 0
        
        list_zx_kouzi = []

        for href in item_href:
            
            url_zx_kouzi = r"https://www.zhongxinwanka.com/%s"%href
            rq_zx_kouzi = load_page4(url_zx_kouzi, headers_zx)
            selector = etree.HTML(rq_zx_kouzi)
       
            item_name = selector.xpath("//span[@id='thread_subject']/text()")
            print(item_name)
            
            aa = selector.xpath("//ul[@class='deankviewul']/li[2]/div[@class='deankuanlic']/span/text()")
            item_term = isempty(aa)
                    
            bb = selector.xpath("//ul[@class='deankviewul']/li[1]/div[@class='deankuanlic']/span/text()")
            item_amount = isempty(bb)
            
            cc = selector.xpath("//ul[@class='deankviewul']/li[3]/div[@class='deankuanlic']/span/text()")
            item_cost = isempty(cc)
            
            ee = selector.xpath("//script[@type='application/ld+json']/text()")
            eee = isempty(ee)
            #print(eee)
            item_uptime = json.loads(ee[0])["upDate"][:10]
            #print(item_uptime) 
                    
            row = [
                item_name[0], 
                item_term[0], 
                item_amount[0], 
                item_cost[0], 
                item_uptime
                ]
                
            list_zx_kouzi.append(row)
            
            n+=1
            print(n)
            print(href, num)
        
        write("zhongxin", list_zx_kouzi) 
 

def clean_word(text):
    new = []
    for i in text:
        new.append(i.replace(" ","").replace("\n","").replace("\r",""))
    
    return new
        
#互金协会项目信息        
def hujin_pro(): 
    
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}  
    
    rows  = []              

    url = "https://dp.nifa.org.cn/HomePage?method=getProjectsInfo"
    html = load_page3(url,headers)
    #print(html)
    selector = etree.HTML(html)
    
    aa = selector.xpath("//tbody[@id='runinfotbody']/tr/td[1]/a/text()")
    item_pt_name = clean_word(aa)
    
    bb = selector.xpath("//tbody[@id='runinfotbody']/tr/td[2]/a/text()")
    item_company = clean_word(bb)
    
    cc = selector.xpath("//tbody[@id='runinfotbody']/tr/td[3]/a/text()")
    item_project_name = clean_word(cc)
    
    dd = selector.xpath("//tbody[@id='runinfotbody']/tr/td[4]/text()")
    item_project_amount = clean_word(dd)
    
    ee = selector.xpath("//tbody[@id='runinfotbody']/tr/td[5]/text()")
    item_project_status = clean_word(ee)
    
    ff = selector.xpath("//tbody[@id='runinfotbody']/tr/td[6]/text()")
    item_project_term = clean_word(ff)
     
    gg = selector.xpath("//tbody[@id='runinfotbody']/tr/td[7]/text()")
    item_project_rate = clean_word(gg)
    
    hh = selector.xpath("//tbody[@id='runinfotbody']/tr/td[8]/text()")
    item_project_starttime = clean_word(hh)
    
    ii = selector.xpath("//tbody[@id='runinfotbody']/tr/td[9]/a/@href")
    item_project_detail_link = clean_word(ii)
    
    fetch_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    
    for num in range(0,len(item_pt_name)-1):
        row = [
            fetch_time,   
            item_pt_name[num],
            item_company[num],
            item_project_name[num],
            item_project_amount[num],
            item_project_status[num],
            item_project_term[num],
            item_project_rate[num],
            item_project_starttime[num],
            item_project_detail_link[num]
            ]
    
        rows.append(row)
        
    #write("hujin", rows)
    
    
def fir():
     
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}  
    url = r"https://download.fir.im/hdv9"
    rq = load_page3(url, headers)
    app_info = json.loads(rq)
    print(app_info)
    
    
#爱卡网
#https://www.7177.cn/daikuanchaoshi
#url = "https://www.7177.cn/kz/233/"
#第2个for循环里取口子detail时取巧了，没有一个个取，实际中大部分口子都是每项都有的，但有小部分是有缺失的。爬完自己处理一下
def aikawang():
            
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}  
   
    for page in range(1,288):
        
        url = "https://www.7177.cn/plugin.php?id=hl_wangdai&page={0}".format(page)
        html = load_page3(url, headers)  
        
        rows  = []
    
        selector = etree.HTML(html)
        
        aa = selector.xpath("//td[@class='action']/a/@href")
        links = clean_word(aa)    
        
        
        for link in links:
            
            print(page, link)
            
            url_detail = "https://www.7177.cn{0}".format(link)
    
            html_detail = load_page3(url_detail, headers) 
            
            selector = etree.HTML(html_detail)
            
            bb = selector.xpath("//div[@class='moreinfo']/table/tbody/tr/td/i/text()")
            detail = clean_word(bb)
             
            cc = selector.xpath("//img[@class='logo']/@src")
            
            c = cc[0].find("/20")+1

            if c == 0 :
                online_time = "null"
            else:         
                online_time = cc[0][c:c+4] + "/" + cc[0][c+4:c+9]

            detail.extend([online_time, link])

            rows.append(detail)
            
        write("aikawang", rows)
        
        time.sleep(random.randint(5, 8))

        
#http://www.chakahao.com/cardbin/html/940050.html
#load_page3 解码"gbk"    
def bank_card_info():
    
    path = r"C:\Users\***\Desktop\bank_num.csv"
    bank_num = read_2_csv(path)
    links = [i[0].replace("\ufeff", "") for i in bank_num]

    path = r"C:\Users\***\Desktop\bank_card_info_2019-05-30.csv"
    bank_530 = read_2_csv(path)
    dele = [ii[5].replace("\ufeff", "") for ii in bank_530]

    links = list(set(links) - set(dele))
    #print(links)
        
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
              Chrome/64.0.3282.186 Safari/537.36"}  
    
    try:
        for link in links:
            
            print(link)
            
            url = "http://www.chakahao.com/cardbin/{0}".format(link)
            html = load_page3(url, headers)
            
            if "无法找到该页" not in html:
                
                selector = etree.HTML(html)
                
                aa = selector.xpath("//div[@class='chalist']/p[1]/text()")
                aa = clean_word(aa)[0]
                index_aa = aa.find("卡是")
                debit_credit = aa[index_aa+2:]
                
                bb = selector.xpath("//div[@class='chalist']/p[2]/text()")
                bb = clean_word(bb)[0]
                index_bb = bb.find("型是")
                bank_type  = bb[index_bb+2:]
                         
                cc = selector.xpath("//div[@class='chalist']/p[3]/text()")
                cc = clean_word(cc)[0]
                index_cc = cc.find("度为")
                index_cc2 = cc.find("如：")
                num_char = cc[index_cc+2:index_cc+4]
                num_char_ex = cc[index_cc2+2:]
                
                row = [        
                    debit_credit,
                    bank_type,
                    num_char,
                    num_char_ex,
                    link
                ]          
                
                write("bank_card_info", [row])
                
                time.sleep(random.randint(1, 4))
        
    except Exception as e:
        
        print(str(e))
   
        
#http://www.zuanke8.com/home.php?mod=space&uid=533904&do=index
#http://www.zuanke8.com/home.php?mod=space&uid=6968&do=profile 个人资料页 最全
#2019-06-11 最大uid 993291 最小uid 2
#"您指定的用户空间不存在" 
def zuanke():
       
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
        "Cookie": "_uab_collina=156023877583519853668681; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1557804792,1560238776; timestamp=1560247486000; sign=23A789B59DC68BE1EF26C2328E93E992; ki1e_2132_pc_size_c=0; ki1e_2132_saltkey=L0881if8; ki1e_2132_lastvisit=1560244373; ki1e_2132_sendmail=1; ki1e_2132_ulastactivity=1560247988%7C0; ki1e_2132_auth=b255Bjh7qrZtccqLk7g3NM26aDJpeEu6VzhfGz1diZIkmlqPfFLfaQSNW2PoLP%2FarWFLq%2FtQNs18aKIUFoAvmn4j9%2BY; ki1e_2132_lastcheckfeed=877429%7C1560247988; ki1e_2132_checkfollow=1; ki1e_2132_lip=101.230.10.253%2C1560247988; ki1e_2132_connect_is_bind=0; ki1e_2132_nofavfid=1; ki1e_2132_checkpm=1; ki1e_2132_lastact=1560247998%09connect.php%09check; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1560247999; amvid=8a4f84d79d51d0afcfb5ccf67ddb4a98; td_cookie=4100892490"
    }
    
    try:
        for uid in range(6588, 30001):#993291
            
            print(uid)
            
            url = "http://www.zuanke8.com/home.php?mod=space&uid={0}&do=profile".format(uid)
            html = load_page4(url, headers)               
            #print(html)
            
            keywords = ["请重新注册"]
            
            #all函数测试迭代对象中是否所有条件都成立
            #all([True,False,True]) 结果为False
            #any测试是否至少有一个条件成立
            #any([True,False,False]) 结果为True
            
            if all(keyword not in html for keyword in keywords):
                
                selector = etree.HTML(html)
                              
                #回贴数
                aa = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[3]/text()")[0]
                response = aa.replace("回帖数", "").replace(" ","")
                #print(response)

                #主题数
                bb = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[4]/text()")[0]
                topic = bb.replace("主题数", "").replace(" ","")
                #print(topic)
                
                #昵称
                nickname = selector.xpath("//h2[@class='xs2']/a/text()")[0]
                #print(nickname)
                
                #用户组                
                user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[1]/li/span/a/text()")[0]
                #print(user_group)
                
                #注册时间 
                if "在线时间" in html:                            
                    ee = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[2]/text()")[0]
                else:
                    ee = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[1]/text()")[0]
                register_time = ee.replace("注册时间", "")
                #print(register_time)

                #最后访问时间
                if "在线时间" in html: 
                    ff = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[3]/text()")[0]
                else:
                    ff = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[2]/text()")[0]
                last_login_time = ff.replace("最后访问", "")
                #print(last_login_time)
                
                #上次活动时间
                if "在线时间" in html:
                    gg = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[4]/text()")[0] 
                else:
                    gg = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[3]/text()")[0]
                lacst_active_time = gg.replace("上次活动时间", "") 
                #print(lacst_active_time)
                                                    
                #积分数
                if "卖家信用" in html:
                    hh = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[3]/text()")[0]   
                else:   
                    hh = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[2]/text()")[0]
                point = hh.replace("积分", "") 
                #print(point)
                
                #果果数
                if "卖家信用" in html:
                    ii = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[4]/text()")[0]    
                else:    
                    ii = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[3]/text()")[0]
                guo = ii.replace("果果", "") 
                #print(guo)
                
                #好友数
                kk = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[1]/text()")[0]
                friend = kk.replace("好友数", "").replace(" ","")  
                #print(friend)
                
                               
                row = [
                    response, topic, 
                    nickname, user_group, 
                    register_time, last_login_time,
                    lacst_active_time, point,
                    guo, friend, uid
                ]
                
                print(row)
                
                write("zuanke_users_info", [row])
                time.sleep(random.randint(1, 3))
                        
    except Exception as e:
        
        print(str(e))
    
        
if __name__ == '__main__':
      
    #fir()
    
    #互金协会项目信息
    #hujin_pro()
    
    #kanong(30,50,1)
    #kanong_process()    
    
    #合并卡农各进程结果
    #bb = []
    #paths = [
        #"kanong_2019-04-13.csv",
        #"kanong_56_2019-04-13.csv",
        #"kanong_67_2019-04-13.csv",
        #"kanong_78_2019-04-13.csv",
        #"kanong_89_2019-04-13.csv"
        #]
        
    #for path in paths:
        #aa = read_2_csv(r"C:\Users\***\Desktop\%s"%path)
        #bb.extend(aa)
    #write("kanong_90k", bb) 
    
    
    #kashen()
    
    #zhongxin()

    #贷码    
    #daima()
    
    #r360
    #r360()
    
    #钱街
    #qianjie()
    
    #有米管家
    #youmi()
    
    #koko
    #koko()
    
    #2345贷款王
    #dkw2345()
    
    #借点钱贷款
    #jdqdk()
    
    #给你花
    #geinihua()
    
    #北京互金协会逃废债公示名单
    #beijing()
    
    #网贷天眼已暴雷平台名单
    #wdty_blacklist()
    
    #爱卡网
    #aikawang()
    
    #银行卡信息
    #bank_card_info()
    
    #赚客吧注册用户info
    #zuanke()
    
