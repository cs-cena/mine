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

    
#应用json.loads      
def dkgj():
    
    headers = {"User-Agent":"xulugj://4.12.0 (Android;android22;zh_CN;ID:2-821d204430d0413183f89e03519e9ca7-861868034424141-meizu-708d34db466325dd0b4fe0cb98667418)"}
    
    data = {
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
        
    url = "http://loan.mydkguanjia.com/loanCenter/productloan/list"
    
    rp = json.loads(load_page(url, data, headers))
    
    rows = [["平台名字", "预估额度", "综合利率"]]
    
    for qj in rp["data"]["speedCompanyList"]["records"]:
        
        name = qj["companyName"] #平台名字
        amount = qj["estimateAmount"] #预估额度
        rate = qj["complexRate"] #综合利率
        
        row = [name, amount, rate]

        rows.append(row)
    
    print(rows)
    
    
#应用json.load
#fiddler直接保存entire response，去除报头。##内容拉到最后有0，注意删掉##
#https://static.huaqianwy.com/api/product/filter  有5个
def dkw2345():    
    
    #需拖动，有好几个，拉一次显示10个保存一次
    rows = [["平台名字", "额度", "期限", "综合利率", "条件"]]
    
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
                
            rows.append(row)
    
    write("2345dkw",rows)
    
    
    
#北京互金协会逃废债公示名单    
#在网页上抓这个url，看responce拉到最后可以看总数
def beijing():    
    
    url = "https://www.bjp2p.com.cn/malice/queryMaliceList"   
    
    #headers_bj = {"User-Agent":"Mozilla/5.0 (Macintosh;IntelMacOSX10_7_0) AppleWebKit/535.11 (KHTML,like Gecko) \
                 # Chrome/17.0.963.56 Safari/535.11"}

    headers = {
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

    data ={     
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
    
    #with open(r'C:\Users\***\Desktop\bj.json', 'w', encoding='utf-8') as json_file:
        #json.dump(rq_bj, json_file, ensure_ascii=False)
        #print("write json file success!")
    
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
    

#应用时间截取重新格式化   
#爱卡网
#https://www.7177.cn/daikuanchaoshi
#url = "https://www.7177.cn/kz/233/"
#第2个for循环里取口子detail时取巧了，没有一个个取，实际中大部分口子都是每项都有的，但有小部分是有缺失的。爬完自己处理一下
def aikawang():
            
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}  
   
    for page in range(1,360):
        
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
        
        time.sleep(random.randint(3, 8))

#应用all any        
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
    
    
def wulai():
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
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
           

#应用pd.read_html  
def xinyong():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }
    
    ff = []

    for page in range(2, 132):
        
        print(page)
        
        url = r"https://xinyongheimingdan.cc/s?p=%s" % page
        
        html = load_page3(url, headers)        
        #print(html)
        
        data=pd.read_html(html, header=0, encoding='utf-8') 
        ff.append(data[0])
        #print(data)
    p = pd.concat(ff)
    p.to_csv("C:/Users/***/Desktop/xinyong.csv", encoding='utf-8-sig', index=None)       

        
#应用page = [page]*len(aa), for item in list(zip()):
def jinlixinshanxi():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }
    
    for page in range(1, 1615):
        
        print(page)
        
        url = r"http://www.sxjlx.com.cn/index.php/contents/info/plist/siteid/1/page/{0}.html".format(page)
        
        html = load_page3(url, headers)
    
        selector = etree.HTML(html)
        
        #姓名
        aa = selector.xpath("//div[@class='List_lis1']/a/div[@class='List_lis1_zi']/p[1]/text()")
        name = clean_word(aa)
        
        #组织机构代码/身份证号
        bb = selector.xpath("//div[@class='List_lis1']/a/div[@class='List_lis1_zi']/p[2]/text()")
        id_num = clean_word(bb)
               
        #页数
        pages = [page]*len(aa)
        
        rows = []
    
        for item in list(zip(name, id_num, pages)):            
            rows.append(list(item))
    
        write("jinglixin", rows)
        time.sleep(random.randint(0, 1))
              
        
#针对"查看详情"等,先取目标链接,后爬取        
def shandong_court():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }
    
    #44147
    for page in range(5580, 44148):
        
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
         
           
    
def get_pic():
    
    def save_pic(path, pic):          
        with open(path, 'wb') as f:
            f.write(pic)

            
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }    
    
    url_list = [

    ]
    
    x = 1
    for url in url_list:
        pic = requests.get(url, headers=headers).content
        path = r"C:\Users\***\Desktop\shixin_pic\qiongjiang_{0}.jpg".format(x)
        save_pic(path, pic)
        print(x)
        
        time.sleep(random.randint(1, 2))
        x+=1

def get_cookie():
    
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
    

#针对"查看详情"等,先取目标链接,后爬取
def sh_high_court():
    
    def clean(text):
        new = []
        for i in text:
            new.append(i.replace("\xa0",""))    
        return new
    
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Cookie": "td_cookie=3303386247; JSESSIONID=B11C753508C235E5FAFC80D9A1AAF5E4-n1"
    }
    
    #共16392页
    for page in range(1295, 1296):#1290, 16637
        
        print(page)
        
        data = {
            "toPage": page,
            "fydm": "",
            "ah": "",
            "bzxr": ""
        }
        
        #取links
        url = r"http://www.hshfy.sh.cn/shfy/gweb2017/channel_zx_list.jsp?pa=aemw9emJncwPdcssPdcssz"
                
        html = load_page_gbk(url, data, headers)
        
        #print(html)
    
        selector = etree.HTML(html)
        
        aa = selector.xpath(r"//div[@class='list']/div[@class='list_a']/ul/li/a/@href")        
        titles = selector.xpath(r"//div[@class='list']/div[@class='list_a']/ul/li/a/text()")
        
        links = []
        for ii in list(zip(aa, titles)):
            if "公司" not in ii[1]:
                links.append(ii[0])
               
        rows = []
        erro_rows = []
        
        for i in links:
            
            url2 = r"http://www.hshfy.sh.cn/shfy/gweb2017/" + i
            
            html2 = load_page4(url2, headers)
            
            #print(html2)
            
            selector = etree.HTML(html2)
            
            #姓名
            bb = selector.xpath(r"//td[@class='nr']//tr[1]/td[@class='tdnr'][2]/text()")
            print(bb)
            
            if "被执行人地址" in html2:                
                #身份证号
                cc = selector.xpath(r"//td[@class='nr']//tr[5]/td[@class='tdnr'][2]/text()")
                
                #执行案号
                dd = selector.xpath(r"//td[@class='nr']//tr[9]/td[@class='tdnr'][2]/text()")
                
                #立案时间
                ee = selector.xpath(r"//td[@class='nr']//tr[8]/td[@class='tdnr'][2]/text()")
            else:
                #身份证号
                cc = selector.xpath(r"//td[@class='nr']//tr[4]/td[@class='tdnr'][2]/text()")
                
                #执行案号
                dd = selector.xpath(r"//td[@class='nr']//tr[10]/td[@class='tdnr'][2]/text()")
                
                #立案时间
                ee = selector.xpath(r"//td[@class='nr']//tr[11]/td[@class='tdnr'][2]/text()")                
                
            
            if bb:
            
                row1 = [bb[0], cc[0], dd[0], ee[0], str(page)]
                row = clean(row1)                
                #print(row)    
                rows.append(row)
            
            else:
                erro_row = [page, url2]
                erro_rows.append(erro_row)
                
            time.sleep(random.randint(3, 5))
            
        write("sh_high_court", rows)
        if erro_rows:
            write("erro_rows", erro_rows)        
        print("%s done" % page)
        #time.sleep(random.randint(0, 1))
        

def yutu():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }
    
    for page in range(268, 2928):#2928
        
        print(page)
        
        url = r"https://www.yetu.net/product/{0}.html".format(page)
        
        html = load_page3(url, headers)
        
        if "您访问的页面不存在" not in html:
            #print(html)
        
            selector = etree.HTML(html)
            
            #名字
            aa = selector.xpath("//div[@class='name-detail']/div[@class='tit']/h1/text()")
            
            #期限
            bb = selector.xpath("//div[@class='sr-tag']/label[@class='red mr20']/text()")
            if bb:
                bb = bb
            else:
                bb.append("")
                           
            #上线时间
            cc = selector.xpath("//div[@class='sr-list sr-detail fl']/ul/li/div[@class='hd']/img/@src")
            
            c = cc[0].find("/20")+1
    
            if c == 0 :
                online_time = "null"
            else:         
                online_time = cc[0][c:c+10] 
         
            rows = [[aa[0], bb[0], online_time, page]]
            
            write("yutu", rows)
            
            
#应用 pd.read_html              
def anhui_high_court(start_page):
    
    global memory
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)",
        "Cookie": "td_cookie=2874964207; JSESSIONID=21EC5500F5D76A651E46D7145311ACEB"
    }
    
    
    for page in range(start_page, 23503):#23503
    
        ff = []
 
        print(page)
        memory[0] = page
        
        url = r"http://www.ahgyss.cn/ssfw/fymh/1451/zxgk.htm?st=0&q=&sxlx=&bzxrlx=&court_id=&bzxrmc=&zjhm=&ah=&startCprq=&endCprq=&page=%s" % page
        
        html = load_page3(url, headers)        
        #print(html)
        
        data=pd.read_html(html, header=0, encoding='utf-8')
        ff.append(data[0])
        #print(data)
        p = pd.concat(ff)
        # mode='a'追加写入
        p.to_csv("C:/Users/***/Desktop/anhui_high.csv", encoding='utf-8-sig', index=None, mode='a')
        print("done")
        
        time.sleep(random.randint(3, 5))


#应用 html.count("")
def qinghai_shixin():

    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
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
    
    
#广州法院失信被执行人
#http://zxgk.gzcourt.org.cn/#/zxxx/zxbg/1
#post: http://wsla.gzcourt.org.cn/gateway/ssfwapi/ssfw_app/app/bgt
def guangzhou_gongkai():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }
    
    url = r"http://wsla.gzcourt.org.cn/gateway/ssfwapi/ssfw_app/app/bgt"
    
    for page in range(1, 2):#15585
        
        print(page)
        
        data = {
            "ah": "",
            "cid": "5SZA4OJkcLbg9XtJE8Jr5129v2hsJ1Vo",
            "fbsj1": "",
            "fbsj2": "",
            "fydm": "440100",
            "lx": "1",
            "pagerows": "155849",
            "postion": str(page),
            "slfy": "4401",
            "xm": "",
            "zjhm": ""
        }
        
        
        rq = json.loads(load_page(url, data, headers))
        
        #print(html)
        
        rows = []
        for item in rq["data"]:
            aa = item["xm"] #姓名
            bb = item["zjhm"] #证件号
            cc = item["ah"] #案号
            dd = item["larq"][:4] #立案年份
            rows.append([aa, bb, cc, dd, page])
        
        write("guangzhou_gongkai", rows)

        
#成都法院司法公开网
#http://cdfy12368.gov.cn:8141/sfgk/webapp/area/cdsfgk/zxxx/zxbg.jsp
def chengdu():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }
    
    url = r"http://cdfy12368.gov.cn:8141/sfgk/webapp/area/cdsfgk/zxxx/ajax.jsp"
    for page in range(1, 831):#831
        
        print(page)
        
        data = {
            "zh": "",
            "opt": "getSxbzxrList",
            "fydm": "510100",
            "bzxr": "",
            "nd": "",
            "fymc": "成都市中级人民法院",
            "dz": "",
            "xxlx": "1",
            "currentPage": str(page),
            "opt": "getSxbzxrList",
            "xxlx": "1",
            "nd": "",
            "dz": "",
            "zh": "",
            "fymc": "成都市中级人民法院",
            "bzxr": "",
            "fydm": "510100"
        }
        
        html = load_page(url, data, headers)
        #print(html)
        selector = etree.HTML(html)
        
        #2姓名 4号码 6执行案号
        #bg1 bg2 每个tr 8个
        bg2 = [1,3,5,7,9]
        bg1 = [2,4,6,8,10]

        #tr_num = html.count('<tr height="30">')
        #html.count('<tr height="30">')
        #html.count('class=bg1')
        
        rows = []

        for t1 in bg2:
            aa = selector.xpath("//tr[{0}]/td[@class='bg2'][2]/text()".format(t1))
            bb = selector.xpath("//tr[{0}]/td[@class='bg2'][4]/text()".format(t1))
            if bb:
                if len(aa[0]) <= 4:
                    rows.append([aa[0], bb[0], page])
        
        for t2 in bg1:
            cc = selector.xpath("//tr[{0}]/td[@class='bg1'][2]/text()".format(t2))
            dd = selector.xpath("//tr[{0}]/td[@class='bg1'][4]/text()".format(t2))
            if dd:
                if len(cc[0]) <= 4:
                    rows.append([cc[0], dd[0], page])

        time.sleep(random.randint(1, 2))
        
        write("成都法院司法公开", rows)
        
        
def ningbo_xinyong():
    
    headers = {
           "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
    }
    
    #44147
    for page in range(7709, 11663):#
        
        print(page)
        
        data = {
            "xm": "",
            "mc": "",
            "pageIndexfr": "1",
            "pageIndex": str(page),
            "zxrlx": "zrr"
        }
        
        #取unid的值
        url = r"http://www.nbcredit.gov.cn/nbggxyww/bzxr/list"
        
        html = load_page(url, data, headers)
        
        #print(html)
    
        selector = etree.HTML(html)
        
        aa = selector.xpath(r"//div[@id='zrr']//a/@onclick")
        #print(aa)
        
        rows = []
        x = 0 
        for i in aa:            
            if "getDetail" in i:
                index1 = i.find("(") + 2
                index2 = i.find(")") - 1
                unid = i[index1:index2]
        
                #拿unid的值去匹内容
                url2 = r"http://www.nbcredit.gov.cn/nbggxyww/bzxr/getDetail?unid={0}".format(unid)
                
                html2 = load_page3(url2, headers)
                #print(html2)
                detail = etree.HTML(html2)
                
                aaa = detail.xpath("//td/text()")
                #print(aaa) 
                rows.append(aaa)
                x+=1
                print(page, x)
                time.sleep(random.randint(0, 1))
        
        write("ningbo_xinyong", rows)
       

        



if __name__ == '__main__':
      
    #beijing()
       
    '''
    memory = [13301]

    while True: 
        try:            
            start_page = memory[0]
            anhui_high_court(start_page)
            time.sleep(30)            
        except Exception as e:
            print(str(e))
    '''
    
    ningbo_xinyong()
