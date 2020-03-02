import csv
import datetime

def read_csv(path):
    
    with open(path, "r", encoding="utf-8", newline='') as f:
        
        read = csv.reader(f)       
        rows = []
        
        for row in read:
            rows.append(row)
    
    print("导入完成")
            
    return rows
    
    
def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\***\Desktop\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows)    


def clean_appname(app_names):

    for each in app_names:

        need_del_app = [
            "ebay","LV","JQB","PIZZA","https://fir.im/n1hf",
            "369","666","365","520","rmb","新714","贷款3",
            "黑户都下款000","借条下款3000","借条已下款800",
            "黑户已下款980","新高炮下款3000","新口子已到账900",
            "97K","9177","1916","贷款123","ak47","借钱PP",
            "51测试","测试产品","测试的","测试哒","测试通知。",
            "马上帮(未测试）","放水口子","下款口子","高炮口子"
        ]

        if each[0] in need_del_app:            
            each[0] = ""           
            write("kn", [each])

        else:
            new = each[0].replace("·","").replace("+","").replace("：","")\
                        .replace("。","").replace("、","").replace("、","")\
                        .replace("，","").replace(".","").replace("—","")\
                        .replace("%","").replace("app","").replace("-","")\
                        .replace("a","").replace("b","").replace(" ","")\
                        .replace("A","").replace("B","").replace("u","")\
                        .replace("s","").replace("q","").replace("PP","")\
                        .replace("~","").replace("版","").replace("安卓","")\
                        .replace("苹果","").replace("下载","")
    
    
            contain_num_app = [
                "51花1","金12","银91",
                "91好借","双11","91好借0",
                "520","51速借A","91随便花",
                "100元"
            ]

            if new not in contain_num_app:
                if all(keyword not in new for keyword in ["51","91"]):
                    new = new.replace("1","").replace("2","")
        
                
            if "（" in new:
                new = new[:new.find("（")]
            elif "【" in new:
                new = new[:new.find("【")]
            elif "(" in new:
                new = new[:new.find("(")]


            each[0] = new            
            write("kn", [each])
                  
                  
if __name__ == '__main__':
    
    path = r"C:\Users\***\Desktop\kanong_2020-02-27.csv"
    app_names = read_csv(path)
    
    clean_appname(app_names)
