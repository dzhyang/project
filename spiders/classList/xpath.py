import requests
from lxml import etree

url = " https://movie.douban.com/cinema/nowplaying/kunming/"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36",
    "Referer": "https://movie.douban.com/tv/"
}
response = requests.get(url, headers=header)

ret = response.content.decode()

#print(ret)

html = etree.HTML(ret)
#print(html)

name_list =   html.xpath("//div[@id='nowplaying']//ul[@class='lists']/li/@data-title")
adress_list = html.xpath("//div[@id='nowplaying']//ul[@class='lists']//li[@class='poster']/a/@href")
img_list=     html.xpath("//div[@id='nowplaying']//ul[@class='lists']//li[@class='poster']//img/@src")
#print(name_list)
#print(adress_list)
#print(img_list)
with open("NewMovie.csv", "w", encoding="gbk") as f:
    num=0
    while num<len(name_list):
        f.write("电影名:"+name_list[num]+","+"网址："+adress_list[num]+","+"图片地址："+img_list[num]+"\n")
        num += 1
        

