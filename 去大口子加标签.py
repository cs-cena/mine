
import datetime
import csv


def clean_word(text):
    new = []
    for i in text:
        new.append(i.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace("\xa0",""))
    
    return new
    
    
def read_csv(path):
    
    with open(path, "r", encoding="utf-8", newline='') as f:
        
        read = csv.reader(f)
        rows = []
        
        for row in read:          
            rows.append(row[0])#[[],[]...] row[0] 第一列
    
    print("导入完成")
            
    return rows
   
    
#指定路径为桌面
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\***\Desktop\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows)

        
#不指定路径
def write_csv(path, rows):
    
    today = datetime.date.today()

    with open(path, "a", encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f) 
        writer.writerows(rows)
        
        
#注意要将需读取的csv文件，转码为 utf-8 无BOM格式 不然第一列会有\ufeff
#new_dc_apps格式 ["口子1","口子2","口子3"]
#需要标注每日新口子/新口子
#按天分开传入
def clean_daichao_app(new_dc_apps, date):
     
    #读取大口子app
    big_apps = set(read_csv(r"\***\大口子APP.csv"))
    #贷超口子去重
    distinct_dc_apps = set(new_dc_apps)
    #去除大口子
    clean_dc_apps = distinct_dc_apps - big_apps
    
    #需要根据触碰贷超存量的数量，来标注每日新口子(0次)/新口子(>0次),并添加当日时间"YYYY-MM-DD"
    saved_dc_apps = set(read_csv(r"\***\贷超APP.csv"))
    
    #标注每日新口子(0次)
    daily_new_dc_apps = clean_dc_apps - saved_dc_apps
    done_daily_new_dc_apps = [[each.replace(" ", ""), "每日新口子", date] for each in list(daily_new_dc_apps)]
    #print(done_daily_new_dc_apps)
    
    #标注新口子(>0次)
    old_dc_apps = clean_dc_apps - daily_new_dc_apps
    done_old_dc_apps = [[each.replace(" ", ""), "新口子", date] for each in list(old_dc_apps)]
    #print(done_old_dc_apps)
    
    #合并
    results = []
    results.extend(done_daily_new_dc_apps)
    results.extend(done_old_dc_apps)
    
    #把要传的保存在桌面
    write("dc_apps", results)
    #保存进存量
    write_csv(r"\***\贷超APP.csv", results)
    
    
# new_lt_apps格式 [["代尔富","3"],[...]]
def luntan_app(new_lt_apps, date):
    
    #读取大口子app
    big_apps = read_csv(r"\***\大口子APP.csv")
    #去除大口子
    results = [[each[0].replace(" ", ""), each[1], date] for each in new_lt_apps if each[0] not in big_apps]
            
    #把要传的保存在桌面
    write("lt_apps", results)
    #保存进存量
    write_csv(r"\***\论坛APP.csv", results)
    
    
if __name__ == '__main__':
    
#    #清洗贷超app   
#    #new_dc_apps格式 ["口子1","口子2","口子3"]
#    date = "2020-05-18"
#    new_dc_apps = [
#    ]
#
#    clean_daichao_app(new_dc_apps, date)

    
#    #清洗论坛app
#    #new_lt_apps格式 [["代尔富","3"],[...]]  
#    date = "2020-05-13"
#    new_lt_apps = [
#                   
#                   ]
#    
#    luntan_app(new_lt_apps, date)

    
