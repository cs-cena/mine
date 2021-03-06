import requests
import datetime
import time
import random
import json
import csv


def load_page3(url, headers):

    response = requests.get(url, headers=headers)#

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text
   
    
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\***\Desktop\bd\%s_%s.csv" % (pt_name, today), "a", encoding= "utf-8-sig", newline='') as f:
        writer = csv.writer(f) 
        writer.writerows(rows)
        
        
def read_csv(path):
    
    with open(path, "r", encoding="utf-8", newline='') as f:
        
        read = csv.reader(f)       
        rows = []
        
        for row in read:          
            rows.append(row[0].replace("\ufeff", ""))#不加[0]则是添加单个列表元素如[""]
    
    print("导入完成")
            
    return rows
           
    
def bd_shixin(last_name, file_name, name_index):
    
    global memory
    
    headers = {
        "Host": "sp0.baidu.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=95943715_hao_pg&wd=%E8%80%81%E8%B5%96&oq=%25E8%2580%2581%25E8%25B5%2596&rsv_pq=ec5e631d0003d8eb&rsv_t=b295wWZB5DEWWt%2FICZvMsf2TZJVPmof2YpTR0MpCszb28dLtEQmdjyBEidZohtPIr%2FBmMrB3&rqlang=cn&rsv_enter=0&prefixsug=%25E8%2580%2581%25E8%25B5%2596&rsp=0&rsv_sug9=es_0_1&rsv_sug=9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    
       
    for page in range(0, 101):
        
        print(page, last_name, name_index)
        
        url = r"https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&cardNum=&iname=" +last_name+r"&areaName=&pn="+str(page*10)+r"&rn=10&ie=utf-8&oe=utf-8&format=json"
        
        rq = json.loads(load_page3(url, headers))
        #print(rq)
        
        #rows = [["发布时间时间戳", "发布时间", "被执行人姓名", "身份证号/公司工商号", "年龄",
                 #"执行法院", "省份", "具体失信行为", "案件号", "执行情况", "页数"]]
        rows = []
        
        if rq["data"]:

            for ii in rq["data"]:
                kkk = ii["result"]
                for item in kkk:
                    ee = item["iname"], #被执行人姓名
                    if len(ee[0]) <= 4:
                        aa = item["age"],#年龄
                        bb = item["publishDate"],#发布时间
                        cc = item["courtName"], #执行法院
                        dd = item["publishDateStamp"],#发布时间时间戳
                        ff = item["areaName"],#省份
                        gg = item["disruptTypeName"],#具体失信行为
                        hh = item["caseCode"],#案件号
                        jj = item["cardNum"],#身份证号/公司工商号
                        kk = item["performance"]#执行情况
                    
                        row = [dd[0], bb[0], ee[0], jj[0], aa[0], cc[0], ff[0], gg[0], hh[0], kk, page, last_name]
        
                        rows.append(row)
                        #print(row)
                        
            write(file_name, rows)
        
        if page%2 == 0: 
                time.sleep(random.randint(1, 2))

                
if __name__ == '__main__':
    
    #页数 pn=0 第一页 pn=10 第二页 
    #name_inde从0开始
    memory = ["振", 530]
    file_names = ["bd_shixin"]

    try:
        #last_names = ["赵","钱","孙","李","周","吴","郑","王","冯","陈","褚","卫","蒋","沈","韩","杨","朱","秦","尤","许","何","吕","施","张","孔","曹","严","华","金","魏","陶","姜","戚","谢","邹","喻","柏","水","窦","章","云","苏","潘","葛","奚","范","彭","郎","鲁","韦","昌","马","苗","凤","花","方","俞","任","袁","柳","鲍","史","唐","费","廉","岑","薛","雷","贺","倪","汤","滕","殷","罗","毕","郝","邬","安","常","乐","于","时","傅","皮","卞","齐","康","伍","余","元","卜","顾","孟","平","黄","和","穆","萧","尹","姚","邵","舒","汪","祁","毛","禹","狄","米","贝","明","臧","计","伏","成","戴","谈","宋","茅","庞","熊","纪","屈","项","祝","董","杜","阮","蓝","闵","席","季","麻","强","贾","路","娄","危","江","童","颜","郭","梅","盛","林","刁","钟","徐","邱","骆","高","夏","蔡","田","樊","胡","凌","霍","虞","万","支","柯","管","卢","莫","经","房","裘","缪","干","解","应","宗","宣","丁","贲","邓","郁","单","杭","洪","包","诸","左","石","崔","吉","钮","龚","程","嵇","邢","滑","裴","陆","荣","翁","荀","羊","於","惠","甄","加","封","芮","羿","储","靳","汲","邴","糜","松","井","段","富","巫","乌","焦","巴","弓","牧","隗","山","谷","车","侯","宓","蓬","全","郗","班","仰","秋","仲","伊","宫","宁","仇","栾","暴","甘","钭","厉","戎","祖","武","符","刘","詹","束","龙","叶","幸","司","韶","郜","黎","薄","印","宿","白","怀","蒲","台","从","鄂","索","咸","籍","赖","卓","蔺","屠","蒙","池","乔","阴","胥","能","苍","双","闻","莘","党","翟","谭","贡","劳","逄","姬","申","扶","堵","冉","宰","郦","雍","璩","桑","桂","濮","牛","寿","通","边","扈","燕","冀","郏","浦","尚","农","温","别","庄","晏","柴","瞿","阎","充","慕","连","茹","习","宦","艾","鱼","容","向","古","易","慎","戈","廖","庚","终","暨","居","衡","步","都","耿","满","弘","匡","国","文","寇","广","禄","阙","东","殳","沃","利","蔚","越","夔","隆","师","巩","厍","聂","晁","勾","敖","融","冷","訾","辛","阚","那","简","饶","空","曾","毋","沙","乜","养","鞠","须","丰","巢","关","蒯","相","查","后","红","游","竺","权","逯","盖","益","桓","公","晋","楚","法","汝","鄢","涂","钦","缑","亢","况","有","商","牟","佘","佴","伯","赏","墨","哈","谯","笪","年","爱","阳","佟","琴","言","福","百","家","姓","续","岳","帅"]
        #起名高频词
        last_names = read_csv(r"C:\Users\***\Desktop\姓名统计\first_names_2019-11-05.csv")
        name_index = last_names.index(memory[0])

        for last_name in last_names[name_index:]:
            
            memory[0] = last_name
            name_index = last_names.index(last_name)
            memory[1] = name_index

            if name_index%50 == 0:
                file_name = "bd_shixin_" + str(name_index)
                file_names[0] = file_name
            else:
                file_name = file_names[0]
                
            bd_shixin(last_name, file_name, name_index)
            time.sleep(20)
            
    except Exception as e:
        print(str(e))
    
