#要操作关系数据库，首先需要连接到数据库，一个数据库连接称为Connection；
#连接到数据库后，需要打开游标，称之为Cursor，通过Cursor执行SQL语句，然后，获得执行结果

import sqlite3 as sq
import csv
import pandas as pd


if __name__ == '__main__':
    #数据库地址  
    #r'C:\Users\Administrator\Desktop\Model\restaurant\restaurant.db'
    file_path = r'C:\Users\Administrator\Desktop\finance\finance.db'

    conn = sq.connect(file_path)
    cur = conn.cursor()

    print("Opened database successfully")

    cur.execute(
    '''

    '''
    )

    #print(cur.fetchall())

    cur.close()
    conn.commit()
    conn.close()
