import requests
from lxml import etree
import datetime
import time
import random
import csv


def write(pt_name, rows):
    
	today = datetime.date.today()

	with open(r"C:\Users\***\Desktop\%s_%s.csv"%(pt_name, today), "a",
			encoding="utf-8-sig", newline='') as f:

		writer = csv.writer(f) 
		writer.writerows(rows)


def load_page3(url, headers):

	response = requests.get(url, headers=headers)#, verify=False

	text = response.content.decode("utf-8", 'ignore')#utf-8

	#print(text)
	return text


def clean_word(text):
	new = []
	for i in text:
		new.append(i.replace("m²","").replace("\n","").replace("\r","").replace("元/",""))

	return new


if __name__ == '__main__':


	headers = {
		"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"
	}
    


	for page in range(1, 4):


		url = r"https://shanghai.anjuke.com/sale/o3-p{0}-rd1/?kw=%E4%B8%9C%E6%AC%A3%E5%B0%8F%E5%8C%BA".format(page)

		html = load_page3(url, headers)

		#print(html)

		selector = etree.HTML(html)

		#标题
		#aa = selector.xpath("//a[@class='houseListTitle']/@title")
		#print(aa)

		#户型 室厅
		bb = selector.xpath("//div[@class='house-details']/div[@class='details-item'][1]/span[1]/text()")
		#print(bb)

		#大小
		ccc = selector.xpath("//div[@class='house-details']/div[@class='details-item'][1]/span[2]/text()")
		#print(cc)
		cc = clean_word(ccc)

		#总楼层
		dd = selector.xpath("//div[@class='house-details']/div[@class='details-item'][1]/span[3]/text()")
		#print(dd)

		#建造年份
		ee = selector.xpath("//div[@class='house-details']/div[@class='details-item'][1]/span[4]/text()")
		#print(ee)

		#小区名 地址
		#fff = selector.xpath("//div[@class='house-details']/div[@class='details-item']/span[@class='comm-address']/text()")
		#ff = clean_word(fff)
		#print(ff)

		#总价
		gg = selector.xpath("//li[@class='list-item']/div[@class='pro-price']/span[@class='price-det']/strong/text()")
		#print(gg)

		#元/平米
		hhh = selector.xpath("//li[@class='list-item']/div[@class='pro-price']/span[@class='unit-price']/text()")
		#print(hh)
		hh = clean_word(hhh)

		#link
		#ii = selector.xpath("//div[@class='house-title']/a[@class='houseListTitle']/@href")
		#print(ii)

		content = zip(bb, cc, dd, ee, gg, hh)

		today = datetime.date.today()

		rows = [list(kk) for kk in content]

		#print(rows)

		write("ajk", rows)



