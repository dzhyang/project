import requests,re,csv,multiprocessing
from lxml import etree
import math as m
import numpy as np

def get_page(url,h):
	try:
		r = requests.get(url, headers=h, timeout=10)
		if r.status_code == 200:
			result=etree.HTML(r.text)
			return result  # 请求成功，返回已解析网页代码
		else:
			return None
	except Exception as e:
		print('\n获取 %s 失败，稍后重试\n' % url)
		return None

def secondary_page_url(page):
	return page.xpath("//ul[@class='listContent']//a[@class='img']/@href")

def get_info(page):
	info_1=[]

	codes = [
		r"""page.xpath("//div[@class='wrapper']/text()")[0].split(' ')[0]""",#小区名称
		r"""page.xpath("//div[@class='deal-bread']/a/text()")[2]""",#区域
		r"""page.xpath("//div[@class='deal-bread']/a/text()")[3]""",#区域
		r"""re.search(r"resblockPosition:'(.*?),(.*?)'", etree.tostring(page).decode()).group(1)""",#经度
		r"""re.search(r"resblockPosition:'(.*?),(.*?)'", etree.tostring(page).decode()).group(2)""",#纬度
		r"""page.xpath("//div[@class='wrapper']/span/text()")[0].split(' ')[0]""",#成交时间
		r"""page.xpath("//div[@class='price']//i/text()")[0]""",#成交价
		r"""page.xpath("//div[@class='price']//b/text()")[0]"""#单价
	]
	for code in codes:
		try:
			info_1.append(eval(code))
		except Exception as e:
			info_1.append(np.NaN)

	info_2=[]
	for i in range(6):#挂牌价格 成交周期 调价 带看 关注 浏览
		try:
			info_2.append(page.xpath("//div[@class='msg']//label")[i].xpath("text()")[0])
		except Exception as e:
			info_2.append(np.NaN)

	info_3 = []
	for i in range(20):#基本信息
		try:
			info_3.append(page.xpath("//div[@class='introContent']//li")[i].xpath("text()")[0].strip())
		except Exception as e:
			info_3.append(np.NaN)
	return [*info_1, *info_2, *info_3]
	

def get_main_page(url,h,page,area):
	print("爬取%s区域的第%d页列表" % (area, page))
	secondary_pages=[]
	main_page = get_page(url+ area + "/" + "pg" + str(page) + "/", h)
	if main_page!=None:
		secondary_pages.extend(secondary_page_url(main_page))
	data=[]
	print("爬取%s区域第%d页的详细信息"%(area, page))
	for secondary_page in secondary_pages:
		page = get_page(secondary_page, h)
		if page!=None:
			data.append(get_info(page))
	print("当前爬取数量：%d" % len(data))
	return data


def writer_csv(dataset):
	try:
		f = open("./data.csv", 'a', newline='', encoding='gbk')
		writer = csv.writer(f)
		for data in dataset:
			writer.writerow(data)
		print("已写入%d条数据" %len(dataset))
	except Exception as e:
		print(e)
	finally:
		f.close()

if __name__ == "__main__":
	start_url="https://km.lianjia.com/chengjiao/"
	areas = ["wuhua", "panlong", "guandu", "xishan23", "chenggong"]
	h = {
		"Host": "km.lianjia.com",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
	}
	columns = ['楼盘名称','区域','子区域','经度','纬度','成交时间','成交价','成交单价','挂牌价格','成交周期','调价','带看','关注','浏览',
			'房屋户型','所在楼层','建筑面积','户型结构','套内面积','建筑类型','房屋朝向','建成年代','装修情况','建筑结构',
			'供暖方式','梯户比例','产权年限','配备电梯','链家编号','交易权属','挂牌时间','房屋用途','房屋年限','房权所属']
	f = open("./data.csv", 'w', newline='', encoding='gbk')
	writer = csv.writer(f)
	writer.writerow(columns)
	f.close()
	miss_main_pages = []
	miss_secondary_pages = []
	all_secondary_page = []
	pagenums=[]
	p = multiprocessing.Pool(50)
	for area in areas:
		url = start_url + area + "/"
		_max = get_page(url,h)
		if _max != None:
			pagenums.append(m.ceil((int)(_max.xpath("//div[@class='total fl']/span/text()")[0])/30))
			print(pagenums)
	
	for n in range(0,5):
		i=1
		while(i<=pagenums[n]):
			p.apply_async(get_main_page, (start_url, h, i, areas[n]),callback=writer_csv)
			i+=1
	p.close()
	p.join()

