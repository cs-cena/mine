import os
import csv
import datetime
import pandas as pd

def creat_df(path_source, names):
    
    dfs = []
    
    for i in os.listdir(path_source):
        path = path_source + "\{0}".format(i)
        df = pd.read_csv(path, names=names)
        dfs.append(df)
        
    df1 = pd.concat(dfs)
    
    return df1
        
    
def shandong():
    
    path_source = r"C:\Users\***\Desktop\shandong\ss"
    names = ["姓名","证件号码","案件号","判决法院","公布时间","id","页数"]

    df = creat_df(path_source, names)
    
    df2 = df[["姓名","证件号码"]]
    # ~ 表示取反
    #df3 = df2.loc[~df2['姓名'].str.contains("公司")]
    #df5 = df4[(df4["姓名"].str.len() < 5)]
    df3 = df2[(df2["证件号码"].str.len() == 18) & (df2["姓名"].str.len() < 5)]
    #index=None 不加索引列
    df3.to_csv(r"C:\Users\***\Desktop\1.csv", encoding="utf-8-sig", index=None)

    
def anhui_high():
    
    path_source = r"C:\Users\***\Desktop\anhui_high"
    names = ["序号","姓名/名称","证件号码/组织机构代码","被执行人公布类型","执行案号","执行法院"]

    df = creat_df(path_source, names)
    #-号可以去删除符合条件的指定行
    df1 = df[-df1["姓名/名称"].isin(["姓名/名称"])]
    df2 = df1[(df1["证件号码/组织机构代码"].str.len() == 18) & (df1["姓名/名称"].str.len() < 5)]    
    df3 = df2[["姓名/名称", "证件号码/组织机构代码"]]
    df3.to_csv(r"C:\Users\***\Desktop\1.csv", encoding="utf-8-sig", index=None)  

    
def clean_name():  
    names = [
         "1"#,"2","3","4","5","6","7","8","9","10","11","12"
    ]
         
    path_source = r"C:\Users\***\Desktop\bbb"
    
    creat_df(path_source, names)
    
    df2 = df[["1"]]
    df2 = df2[(df2["1"].str.len() < 5)]    
    df3 = df2.drop_duplicates(["1"])
    
    df3.to_csv(r"C:\Users\***\Desktop\1.csv", mode='a', encoding="utf-8-sig", index=None, header=None)    

def temp():
    path_source = r"C:\Users\***\Desktop\1"
    names = ["1","2","3"]

    df = creat_df(path_source, names) 
    df2 = df[["1", "2"]]
    df3 = df2[(df2["2"].str.len() == 18) & (df2["1"].str.len() < 5)]
    df4 = df3.drop_duplicates(["1","2"])
    df4.to_csv(r"C:\Users\***\Desktop\1.csv", mode='a', encoding="utf-8-sig", index=None, header=None)
    
if __name__ == '__main__':  
  
    #shandong()
    
    #anhui_high()
    
    #clean_name()
    
    path_source = r"C:\Users\Administrator\Desktop\1"
    names = [
    "交易日期", "交易时间", "支出",
    "存入", "余额", "交易类型",
    "交易备注", "大类", "明细"
    ]
    
    df = creat_df(path_source, names)
