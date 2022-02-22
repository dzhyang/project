import json
import re
import requests
from lxml import etree
import random
import extension as ex
#登录
def Login(username,password):
	ip = "http://202.203.158.158"
	Login_IsTrue = "http://202.203.158.158/sso/ssoLogin"
	Login_url = "http://202.203.158.158/sso/login?service=http://202.203.158.158/j_spring_cas_security_check"
	request_Login = requests.Session()
	response_Get_FirstCookies = requests.Response
	#第一次请求，获取cookies
	response_Get_FirstCookies = request_Login.get(ip, allow_redirects=True)

	# print(response_Get_FirstCookies.status_code)  #返回状态码
	# print(response_Get_FirstCookies.headers["Location"])  #下一次请求网址

	# #第一次重定向
	# response = request_Login.get(response_Get_FirstCookies.headers["Location"], allow_redirects=False)
	# print(response.status_code)  #返回状态码
	# print(response.headers["Location"])  #下一次请求网址

	# #第二次重定向
	# response = request_Login.get(response.headers["Location"], allow_redirects=False)
	# print(response.status_code)  #返回状态码

	return_value=ex.JS("./PasswordMD5.js","hex_md5",password)

	data_IsTrue = {"username": username, "password": return_value}
	#检测登录密码是否正确
	response_PassWord_IsTrue = request_Login.post(Login_IsTrue, data=data_IsTrue)
	print(json.loads(response_PassWord_IsTrue.text))

	data_Login = {
		"username": username,
		"password": return_value,
		"lt": "e1s1",
		"_eventId": "submit"
	}
	#登陆请求,获取登陆成功的cookies
	response_Get_LoginSucessCookies = request_Login.post(Login_url, data=data_Login, allow_redirects=True)
	# print(response_Get_LoginSucessCookies.status_code)
	# print(response_Get_LoginSucessCookies.cookies)
	# print(response_Get_LoginSucessCookies.headers["Location"])  #下一次请求网址

	# #第一次重定向
	# response = request_Login.get(response_Get_LoginSucessCookies.headers["Location"], allow_redirects=False)
	# print(response.status_code)  #返回状态码
	# print(response.headers["Location"])  #下一次请求网址

	# #第二次重定向
	# response = request_Login.get(response.headers["Location"], allow_redirects=False)
	# print(response.status_code)  #返回状态码
	# print(response.headers["Location"])  #下一次请求网址

	# #第三次正式请求登陆成功网页
	# response = request_Login.get(response.headers["Location"], allow_redirects=False)
	# print(response.status_code)  #返回状态码
	# ##登陆成功
	return request_Login

#获取课程表
def GetClassList(request):
	request_Get_ClassList = requests.session()
	request_Get_ClassList = request
	# header = {
	#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	#     "Accept-Encoding": "gzip, deflate",
	#     "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
	#     "Connection":"keep-alive",
	#     "Upgrade-Insecure-Requests": "1",
	#     "Cache-Control": "no-cache",
	#     "Pragma": "no-cache",
	#     "Referer": "http://202.203.158.106/jwweb/SYS/Main_banner.aspx",
	#     "Host":"202.203.158.106",
	#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
	# }    
	#request_Get_ClassList.headers=header
	response_ClassList = requests.Response

	# response_ClassList_1 = request_Get_ClassList.get("http://202.203.158.106/jwweb/MAINFRM.aspx")
	# response_ClassList_2 = request_Get_ClassList.get("http://202.203.158.106/jwweb/SYS/Main_banner.aspx")
	# response_ClassList_3 = request_Get_ClassList.get("http://202.203.158.106/jwweb/SYS/Main_tools.aspx")
	# response_ClassList_4 = request_Get_ClassList.get("http://202.203.158.106/jwweb/PUB/foot.aspx")

	#request_Get_ClassList.headers=header
	#response_ClassList_5 = request_Get_ClassList.get("http://202.203.158.106/jwweb/frame/menu.aspx",headers=header)
	# response_ClassList_6 = request_Get_ClassList.get("http://202.203.158.106/jwweb/XSXJ/KingosLove.aspx")
	
	response_ClassList = request_Get_ClassList.get("http://202.203.158.106/jwweb/znpk/Pri_StuSel.aspx")
	
	
	html=etree.HTML(response_ClassList.content.decode(encoding="gb2312"))
	hidyzm=html.xpath('//input[@name="hidyzm"]/@value')   
	return_list = random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", 15)
	
	string=""
	for target_list in return_list:
		string = string + target_list

	return_value=ex.JS("./GetClassListMD5.js","md5","10691"+"20190"+string)
	data = {
		"Sel_XNXQ": 20190,
		"rad": 0,
		"px": 0,
		"txt_yzm": "",
		"hidyzm": hidyzm[0],
		"hidsjyzm":return_value
	}
	response_ClassList=request_Get_ClassList.post("http://202.203.158.106/jwweb/znpk/Pri_StuSel_rpt.aspx?m="+string,data=data)
	html_img=etree.HTML(response_ClassList.content.decode(encoding="gb2312"))
	src = html_img.xpath('//img/@src')
	response_ClassList_img = request_Get_ClassList.get("http://202.203.158.106/jwweb/znpk/" + src[0])
	name="Class.jpg"
	with open("./"+name,"wb") as f:
		f.write(response_ClassList_img.content)
		
	print("课表["+name+"]已存入当前工作路径")


#教务系统
def GetStudent(list_all,request):
	request_EduationSystem = requests.session()
	request_EduationSystem = request
	
	response_Get_EduationSystemLoginHref = requests.Response
	response_Get_EduationSystemLoginHref = request_EduationSystem.get("http://202.203.158.158/app/forward.action?id=" + json.loads(list_all)["sysApps"][6]["id"])
	
	result=re.search(r'location.href="(.*?)";', response_Get_EduationSystemLoginHref.content.decode()).group(1)

	response_Get_EductionSystemLoginCookies = request_EduationSystem.get(result)
	GetClassList(request_EduationSystem)


#返回选项列表
def GetOptionList(uer,psw):
	request_Get_OptionList=Login(uer,psw)
	response_OptionList = request_Get_OptionList.get("http://202.203.158.158/app/getAppList.action?t=0.9694602689761159&resultType=json")
	print(response_OptionList.text)
	return response_OptionList.text,request_Get_OptionList
#启动主函数
if __name__ == "__main__":
	u,p=ex.GetInput()
	List,request_Get_OptionList_return=GetOptionList(u,p)
	#GetStudent(List,request_Get_OptionList_return)


