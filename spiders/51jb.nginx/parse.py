# -*- coding: utf-8 -*-
from os import close
from typing import Counter, Dict, List, Type
from lxml.etree import _Element
from lxml import etree

class CommandSyntax:
    def __init__(self) -> None:
        self._command:str#命令
        self._syntax:str#语法
        self._default:str#默认值
        self._description:str#描述
        self._usedfor:str#用于
        self._note:str#备注






# class SyntaxBuilder:
#     def __init__(self) -> None:
#         self._syntaxs:List[CommandSyntax]
#         self._pageDescription:str
#         self.opened=False
#         self._pagestart=False
#         self._analyzes={
#             "h3":self._analyzeH3,
#             "h4":self._analyzeH4,
#             "h5":self._analyzeH5
#         }

#     def _analyzeH3(self,element:_Element):
#         syntaxTitle:str=element.text
#         if syntaxTitle is ".摘要":
#             self._pagestart=True
#         elif syntaxTitle is ".指令":
#             self._pagestart=False
#         elif syntaxTitle is ".变量":
#             pass
#         elif syntaxTitle is ".参考文档":
#             pass


#     def _analyzeH4(self,element:_Element):
#         pass


#     def _analyzeH5(self,element:_Element):
#         pass
#     def open(self,element:_Element)->None:
#         self._syntaxs=[]
#         self.add(element)
#         self.opened=True

#     def add(self,element:_Element)->None:
#         self._syntaxs.append(element)

#     def close(self)->None:
#         self.opened=False

#     def analyze(self)->None:
#         for element in self._syntaxs:
#             self._analyzes[element.tag](element)


#         pass

#     def build(self)->List[CommandSyntax]:
#         pass

# def parseh2(element:_Element):
#     pass








elementType=["h3","h4","h5"]

def analyze(content:str):
    start=0
    end=0
    while True:
        isfind=False
        try:
            end=content.index("\n",start)
        except:
            pass
        for key in ["语法","默认值","使用字段"]:
            if content[start:end].startswith(key):
                start=end+1
                isfind=True
                break
        if not isfind:
            break
    syntax=content[0:start]
    content=content[start:-1]
    return (syntax,content)




def parse(elements:List[_Element])->List[tuple]:
    pageDescription:str
    syntaxs=[]
    currentSyntax=""
    isFirst=True
    contentstr=""
    # syntaxBuilder=SyntaxBuilder()
    elements=list(filter(lambda elem:(elem.tag in elementType) and ((elem.getprevious().tag in elementType) or (elem.getprevious().getprevious().tag == "h2")),elements))
    pageDescription=elements[1].text.split("。")[0]
    index=2
    while index<len(elements):
        element=elements[index]
        if element.tag == "h3":
            syntaxTitle:str=element.text
            if syntaxTitle == "·指令":
                index+=1
                continue
            elif syntaxTitle == "·变量":
                break
            elif syntaxTitle == "·参考文档":
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
    return syntaxs
import xlwt

with open("./template.html","r") as f:
    bs=f.read()
    htmlCore=etree.HTML(bs)
    paths=htmlCore.xpath("//body/*")
    rt=parse(paths)
    
    # with open("./rt.txt",'wb') as f:
    #     for t in rt:
    #      f.write(t[0].encode(encoding="gbk"))
    #      f.write(t[1].encode(encoding="gbk"))
    #      f.write(t[2].encode(encoding="gbk"))

    style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x01  # 水平左对齐
    al.vert = 0x01  # 设置垂直居中
    al.wrap=1
    style.alignment = al
    workbook = xlwt.Workbook(encoding= 'utf-8')

    worksheet = workbook.add_sheet("nginx")
    worksheet.col(3).width=150*20
    worksheet.col(4).width=200*20
    worksheet.col(5).width=600*20

    # row 3  4  5
    for i in range(0,len(rt)):
        t=rt[i]
        worksheet.write(i,3,t[0],style)
        worksheet.write(i,4,t[1],style)
        worksheet.write(i,5,t[2],style)
    worksheet.write_merge(0, len(rt)-1, 1, 1, '具体模块名')
    worksheet.write_merge(0, len(rt)-1, 2, 2, '模块描述')

    workbook.save("./nginx.xls")