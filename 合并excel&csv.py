import os
import csv
import datetime
import pandas as pd
import numpy as np

 
def merge(path_source):
    
    dfs = []

    writer = pd.ExcelWriter(r'C:\Users\***\Desktop\1.xlsx')
    
    for i in os.listdir(path_source):
        print(i)
        if "xlsx" in i:
            path = path_source + "\{}".format(i)
            df = pd.read_excel(path, sheet_name = 0 , header = None)
            num = df.shape[0]
            df["filename"] = [np.nan]*num
            df["filename"]=df["filename"].fillna(i)
            #print(df)
            dfs.append(df)
            
        elif "csv" in i:
            path = path_source + "\{}".format(i)
            df = pd.read_csv(path, header = None)
            num = df.shape[0]
            df["filename"] = [np.nan]*num
            df["filename"]=df["filename"].fillna(i)
            dfs.append(df)
            
    df1 = pd.concat(dfs)
    df1.to_excel(writer, encoding="utf-8-sig", index=None, header = None)  
    writer.save()
    writer.close()
    
if __name__ == '__main__':
    
    merge(r"***\1.待验证")
