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


def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\***\Desktop\kanong_users\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows)
        
        
def load_page4(url, headers):#, proxies

    response = requests.get(url, headers=headers)#, proxies=proxies , verify=False

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text  
       
#http://www.zuanke8.com/home.php?mod=space&uid=533904&do=index
#http://www.zuanke8.com/home.php?mod=space&uid=6968&do=profile 个人资料页 最全
#2019-06-11 最大uid 993291 最小uid 2
#"您指定的用户空间不存在" 
def kanong(save_uid, final_uid):
    
    global save_uids
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        #"Cookie": "_uab_collina=156023877583519853668681; ki1e_2132_saltkey=LZX1FRWR; ki1e_2132_lastvisit=1560402302; ki1e_2132_connect_is_bind=0; ki1e_2132_nofavfid=1; ki1e_2132_atarget=1; ki1e_2132_smile=1D1; ki1e_2132_home_readfeed=1560999856; ki1e_2132_forum_lastvisit=D_19_1560915214D_15_1561108707; ki1e_2132_pc_size_c=0; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1560908754,1561081463,1561340359,1561531484; ki1e_2132_auth=af8eNgj1JEMmAOvKYlmxYPR54XLpiuoUIrjD5Ojp%2FzB9dQCcnXX7%2BJJj5zYuGrzjs36tknX7dr5%2FYlMAHf3h0KYCSpI; ki1e_2132_lip=101.230.10.253%2C1561531492; ki1e_2132_home_diymode=1; td_cookie=1089783863; ki1e_2132_ulastactivity=1561538164%7C0; ki1e_2132_sendmail=1; ki1e_2132_lastact=1561538165%09home.php%09spacecp; ki1e_2132_checkpm=1; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1561538165; ki1e_2132_lastcheckfeed=877429%7C1561538165; ki1e_2132_checkfollow=1; amvid=2ecea077eb04474ade5e91bc85d5a1ce"
    }
    
    try:
        for uid in range(save_uid, final_uid):
            
            print(uid)
            save_uids[0] = uid
            
            url = "https://www.51kanong.com/home.php?mod=space&uid={0}".format(uid)
            
            proxies = {'http': '47.112.80.214:8118'}
            html = load_page4(url, headers)#, proxies 
            #print(html)
            
            keywords = ["用户空间不存在","请重新注册" , "空间已被锁定", "1970-1-1 08:00"]
            
            #all函数测试迭代对象中是否所有条件都成立
            #all([True,False,True]) 结果为False
            #any测试是否至少有一个条件成立
            #any([True,False,False]) 结果为True
            
            if all(keyword not in html for keyword in keywords):
                
                selector = etree.HTML(html)
                              
                #回贴数/
                aa = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[3]/text()")[0]
                response = aa.replace("回帖数", "").replace(" ","")
                #print(response)

                #主题数
                bb = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[4]/text()")[0]
                topic = bb.replace("主题数", "").replace(" ","")
                #print(topic)
                
                #昵称
                cc = selector.xpath("//div[@class='pbm mbm bbda cl'][1]/h2[@class='mbn']/text()")[0]
                index_cc = cc.find("(")
                nickname = cc[:index_cc].replace("\n", "")
                #print(nickname)
                
                #kws = ['color="#00CCFF"', 'color="#CCCCCC"','color="#999999"', 'color="#00CCCC"','color="#00CC00"', 'color="#00CC99"']
                kws = ['冻结', '金融传奇', '禁止访问', '>VIP<', '至尊成员', '等待验证']
                #用户组
                if "会员标志" in html:
                    #print(1)
                    if "管理组" in html:
                        #print(2)
                        if "</font></a></span>" not in html:
                            user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][3]/ul[1]/li[2]//a/text()")[0]
                        else:
                            user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][3]/ul[1]/li[2]//a/font/text()")[0]
                    
                    elif any(kw in html for kw in kws):
                        #print(3)
                        user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][3]/ul[1]/li//a/text()")[0]
                                                    
                    else:
                        #print(4)
                        user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][3]/ul[1]/li//a/font/text()")[0]
                                                          
                elif "管理组" in html:
                    if "</font></a></span>" not in html: 
                        user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[1]/li[2]//a/text()")[0]
                    else:
                        user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[1]/li[2]//a/font/text()")[0]
                                                
                elif any(kw in html for kw in kws):            
                    user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[1]/li//a/text()")[0]
                                                
                else:
                    user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[1]/li//a/font/text()")[0]
                                                
                #print(user_group)
                
                #注册时间 
                if "会员标志" in html:
                    ee = selector.xpath("//div[@class='pbm mbm bbda cl'][3]/ul[@id='pbbs']/li[2]/text()")[0]

                elif "在线时间" in html:                   
                    ee = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[2]/text()")[0]
                                        
                else:
                    ee = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[1]/text()")[0]
                
                register_time = ee.replace("注册时间", "")
                #print(register_time)

                #最后访问时间
                if "会员标志" in html:
                    ff = selector.xpath("//div[@class='pbm mbm bbda cl'][3]/ul[@id='pbbs']/li[3]/text()")[0]
                                        
                elif "在线时间" in html:
                    ff = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[3]/text()")[0]
                                        
                elif "上次活动时间" not in html:
                    ff = ''
                    
                else:
                    ff = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[2]/text()")[0]
                
                last_login_time = ff.replace("最后访问", "")
                #print(last_login_time)
                
                #上次活动时间
                if "会员标志" in html:
                    gg = selector.xpath("//div[@class='pbm mbm bbda cl'][3]/ul[@id='pbbs']/li[4]/text()")[0]
                                        
                elif "在线时间" in html:
                    gg = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[4]/text()")[0] 
                                        
                elif "上次活动时间" not in html:
                    gg = ''
                    
                else:
                    gg = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[3]/text()")[0]
                
                lacst_active_time = gg.replace("上次活动时间", "") 
                #print(lacst_active_time)
                
                #好友数
                hh = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[1]/text()")[0]
                friend = hh.replace("好友数", "").replace(" ","")  
                #print(friend)                
                                  
                #积分数
                ii = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[2]/text()")[0]
                point = ii.replace("积分", "") 
                #print(point)
                
                #贡献数
                jj = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[3]/text()")[0]                  
                achieve = jj.replace("贡献", "") 
                #print(jj)
                
                #vip美金
                kk = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[4]/text()")[0]                  
                dollar = kk.replace("vip美金", "") 
                #print(kk) 
                
                #花贝
                mm = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[5]/text()")[0]                  
                flower_coin = mm.replace("花贝", "") 
                #print(mm)

                #查询币
                #nn = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[7]/text()")[0]                  
                #collect_coin = nn.replace("查询币", "") 
                #print(nn)                
                
                #回贴数,主题数,昵称,用户组,注册时间,最后登录时间,最后发表时间,朋友数,积分数,贡献,vip美金,花贝,uid                               
                row = [
                    response, topic, 
                    nickname, user_group, 
                    register_time, last_login_time,
                    lacst_active_time, friend,
                    point, achieve, dollar,
                    flower_coin, uid

                ]
                
                print(row)
                
                write("kanong_users_info", [row])
                
            if uid%500 == 0: 
                time.sleep(random.randint(5, 8))

    except Exception as e:
        
        print(str(e))
        
        
if __name__ == '__main__':
    #2019-06-28 卡农 最大uid 1030979 注册时间20190628 14:25
    save_uids = [803854, 1039300]#1030979 1031001 33540
    
    while True: 
        
        start = time.time()
        
        save_uid = save_uids[0] + 1
        final_uid = save_uids[1]
        
        #kanong_users_info
        kanong(save_uid, final_uid)
        
        print('总耗时step_href：%.5f秒' % float(time.time()-start))
        print('save_uids: %s' % save_uids[0])
        print('final_uids: %s' % save_uids[1])
        
        if save_uids[0] == save_uids[1]-1:
            break
        
        time.sleep(random.randint(5, 15))#10, 20
        
