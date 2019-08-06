#要操作关系数据库，首先需要连接到数据库，一个数据库连接称为Connection；
#连接到数据库后，需要打开游标，称之为Cursor，通过Cursor执行SQL语句，然后，获得执行结果


import sqlite3 as sq
import csv
import pandas as pd



if __name__ == '__main__':
        
	file_path = r'C:\Users\***\Desktop\project\test_monitor\spider.db'

	conn = sq.connect(file_path)
	cur = conn.cursor()

	print("Opened database successfully")

	cur.execute(
	    '''
	    SELECT 
	        strftime("%m", last_login_time) as month
	        ,count(uid) AS aa
	    FROM zuanke
	    WHERE register_time > '2019-01-01 00:00:01'
	    GROUP BY month
	    ORDER BY month ASC
	    ''')
	
	print(cur.fetchall())

	conn.commit()
	conn.close()
