import os
import csv
import datetime
import pandas as pd


if __name__ == '__main__':

    dfs = []
    
    path_source = r"C:\Users\***\Desktop\shandong\ss"
    
    for i in os.listdir(path_source):   	
        path = r"C:\Users\chensheng\Desktop\shandong\ss\%s" % file
        df = pd.read_csv(path, names=["姓名","证件号码","案件号","判决法院","公布时间","id","页数"])
        dfs.append(df)
            
    df1 = pd.concat(dfs)
    df2 = df1[["name","id"]]
    # ~ 表示取反
    #df3 = df2.loc[~df2['name'].str.contains("company")]
    #df5 = df4[(df4["name"].str.len() < 5)]
    df3 = df2[(df2["id"].str.len() == 18) | (df2["name"].str.len() < 5)]
    #index=None 不加索引列
    df3.to_csv(r"C:\Users\***\Desktop\1.csv", encoding="utf-8-sig", index=None)
