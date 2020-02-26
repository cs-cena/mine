import os
import datetime


#删除图片
for file_dir in [r"C:\Users\Administrator\Desktop\1", r"C:\Users\Administrator\Desktop\2"]:
	for root, dirs, files in os.walk(file_dir, topdown=False):
	    for name in files:
	        os.remove(os.path.join(root, name))

#删除csv文件
file_name = "1_{}.csv".format(datetime.date.today())
os.remove(os.path.join(r"C:\Users\Administrator\Desktop", file_name))
