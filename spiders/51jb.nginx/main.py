import requests,re,time
from typing import List
from lxml.etree import _Element
from lxml import etree
import xlwt
headers={
    "Referer": "http://shouce.jb51.net/nginx/index.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
}

resp=requests.get("http://shouce.jb51.net/nginx/left.html",headers=headers)
content=resp.content.decode(encoding="GB2312")
html=etree.HTML(content)
urlAndTitle=dict(zip(html.xpath("//a/@href"),html.xpath("//a/text()")))

resultdic={}
urlBase="http://shouce.jb51.net/nginx/"
currentMainTitle=''
for (key,item) in urlAndTitle.items():
    if key.startswith("CompilingNginx"):
        continue
    if key.startswith("http") or key.startswith("Optimizations"):
        break
    if "index" in key:
        currentMainTitle=item.split("、")[1].split("（")[0]
        resultdic[currentMainTitle]={}
        if "第三方" in currentMainTitle:
            groups=re.findall(r"<A href=\"(.*?)\" >\d?.\d{1,} (.*?)（",requests.get(urlBase+key,headers=headers).content.decode(encoding="GB2312"))
            for group in groups:
                if "http:" in group[0]:
                    continue
                resultdic[currentMainTitle][group[1]]=urlBase+"3rdPartyModules/"+group[0]
        continue
    title=item.split(" ")[1].split("（")[0]
    resultdic[currentMainTitle][title]=urlBase+key


elementType=["h3","h4","h5"]

def analyze(content:str):
    start=0
    end=0
    while True:
        isfind=False
        try:
            end=content.index("\r\n",start)
        except:
            pass
        for key in ["语法","默认值","使用字段"]:
            if content[start:end].startswith(key):
                start=end+2
                isfind=True
                break
        if not isfind:
            break
    syntax=content[0:start]
    content=content[start:-1]
    return (syntax,content)

def parse(elements:List[_Element]):
    pageDescription:str
    syntaxs=[]
    currentSyntax=""
    isFirst=True
    contentstr=""
    # syntaxBuilder=SyntaxBuilder()
    elements=list(filter(lambda elem:(elem.tag in elementType) and ((elem.getprevious().tag in elementType) or (elem.getprevious().getprevious().tag == "h2")),elements))
    if len(elements) ==0:
        return "",[]
    pageDescription=elements[1].text.split("。")[0]
    index=2
    while index<len(elements):
        element=elements[index]
        if element.tag == "h3":
            syntaxTitle:str=element.text
            if "指令" in syntaxTitle:
                index+=1
                continue
            elif re.search(r"[\u4e00-\u9fa5·]", syntaxTitle) is not None:
                syntax,content=analyze(contentstr)
                syntaxs.append((currentSyntax,syntax,content))
                break
            else:
                if isFirst:
                    syntaxs=[]
                    isFirst=False
                else:
                    #解析
                    s,d=analyze(contentstr)
                    contentstr=""
                    syntaxs.append((currentSyntax,s,d))
                currentSyntax=element.text.replace(" ","")
        else:
            contentstr+=element.xpath("string(.)")

        index+=1 
    return pageDescription,syntaxs

style = xlwt.XFStyle()
al = xlwt.Alignment()
al.horz = 0x01  # 水平左对齐
al.vert = 0x00  # 设置上对齐
al.wrap=1
style.alignment = al
workbook = xlwt.Workbook(encoding= 'utf-8')

worksheet = workbook.add_sheet("nginx")
worksheet.col(3).width=150*20
worksheet.col(4).width=200*20
worksheet.col(5).width=600*20

start=1
end=1
worksheet.write(0,0,"类别",style)
worksheet.write(0,1,"模块",style)
worksheet.write(0,2,"模块描述",style)
worksheet.write(0,3,"命令",style)
worksheet.write(0,4,"用法",style)
worksheet.write(0,5,"备注",style)

for mainTitle,pages in resultdic.items():
    for subTitle,link in pages.items():
        #time.sleep(0.1)
        page=requests.get(link,headers=headers)
        content=page.content.decode(encoding="GB2312")
        htmlCore=etree.HTML(content)
        elements=htmlCore.xpath("//body/*")

        pageDescription,syntaxs=parse(elements)
        if pageDescription=="":
            continue
        # row 3  4  5
        count=len(syntaxs)
        for i in range(0,count):
            syntax=syntaxs[i]
            worksheet.write(end+i,3,syntax[0],style)
            worksheet.write(end+i,4,syntax[1],style)
            worksheet.write(end+i,5,syntax[2],style)

        worksheet.write_merge(end, end+count, 1, 1, subTitle,style)
        worksheet.write_merge(end, end+count, 2, 2, pageDescription,style)
        end=end+count+1
    worksheet.write_merge(start, end-1, 0, 0, mainTitle,style)
    start=end

workbook.save("./nginx.xls")






















