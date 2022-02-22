using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.IO;
using System.Text.RegularExpressions;

namespace dotnet_core
{
    public class Login
    {

        public Login(string UserName,string PassWord)
        {
            this.UserName = UserName;
            this.PassWord = PassWord;
        }

        private readonly string UserName;
        private readonly string PassWord;
        
        private const string Ip = "http://202.203.158.158";
        private const string Login_IsTrue_Url = "http://202.203.158.158/sso/ssoLogin";
        private const string Login_url = "http://202.203.158.158/sso/login?service=http://202.203.158.158/j_spring_cas_security_check";
        private const string Url_List = "http://202.203.158.158/app/getAppList.action?t=0.9694602689761159&resultType=json";

        public  const string Content_Type = "application/x-www-form-urlencoded";

        /// <summary>
        /// 获取登录的所有Cookies，并登录
        /// </summary>
        /// <returns>登录的Cookies</returns>
        public  CookieContainer GetCookies()
        {
            
            HttpWebRequest GetFirstCookie = WebRequest.CreateHttp(Ip);
            GetFirstCookie.CookieContainer = new CookieContainer();
            HttpWebResponse Response_GetFirstCookie = (HttpWebResponse)GetFirstCookie.GetResponse();
            CookieContainer BackCookies= GetFirstCookie.CookieContainer;

            Encryption encryption = new Encryption();

            string PassWord_MD5= encryption.GetMd5(0,PassWord);

            string PostData = "username" + "=" + UserName + "&" + "password" + "=" + PassWord_MD5;


            HttpWebRequest LoginIsTrue = WebRequest.CreateHttp(Login_IsTrue_Url);
            LoginIsTrue.Method = "POST";
            LoginIsTrue.CookieContainer = BackCookies;
            LoginIsTrue.ContentType = Content_Type;
            using (Stream stream = LoginIsTrue.GetRequestStream())
            {
                stream.Write(Encoding.Default.GetBytes(PostData), 0, PostData.Length);
            }
            HttpWebResponse Response_Login_isTrue = (HttpWebResponse)LoginIsTrue.GetResponse();
            Console.WriteLine(new StreamReader(Response_Login_isTrue.GetResponseStream()).ReadToEnd());

            


            string Data_Login = "username"+"="+ UserName+"&"+"password"+"="+ PassWord_MD5+"&"+"lt"+"="+ "e1s1"+"&"+"_eventId" + "=" + "submit";

            HttpWebRequest Login_Sucess_Cookies = WebRequest.CreateHttp(Login_url);
            Login_Sucess_Cookies.CookieContainer = BackCookies;
            Login_Sucess_Cookies.ContentType = Content_Type;
            Login_Sucess_Cookies.Method = "POST";
            using (Stream stream = Login_Sucess_Cookies.GetRequestStream())
            {
                stream.Write(Encoding.Default.GetBytes(Data_Login), 0, Data_Login.Length);
            }

            HttpWebResponse Response_Login_Sucess = (HttpWebResponse)Login_Sucess_Cookies.GetResponse();


            return BackCookies;
        }

        /// <summary>
        /// 统一门户各应用入口
        /// </summary>
        /// <param name="container">登录返回的Cookies</param>
        /// <returns>各应用入口集合</returns>
        public Dic  GetList(CookieContainer container)
        {
            
            HttpWebRequest Get_List = WebRequest.CreateHttp(Url_List);
            Get_List.CookieContainer = container;
            Get_List.ContentType = Content_Type;

            HttpWebResponse Response_List = (HttpWebResponse)Get_List.GetResponse();
            string List_App= new StreamReader(Response_List.GetResponseStream()).ReadToEnd();
            MatchCollection re_id= Regex.Matches(List_App, @"""id"":""(.*?)""");
            MatchCollection re_icon= Regex.Matches(List_App, @"""icon"":""(.*?)""");
            MatchCollection re_name= Regex.Matches(List_App, @"""name"":""(.*?)""");

            Dic List_Dic = new Dic
            {
                { re_id[0].Groups[1].Value, re_icon[0].Groups[1].Value, List_Name.正版软件 },
                { re_id[1].Groups[1].Value, re_icon[1].Groups[1].Value, List_Name.安心付 },
                { re_id[2].Groups[1].Value, re_icon[2].Groups[1].Value, List_Name.学工系统},
                { re_id[3].Groups[1].Value, re_icon[3].Groups[1].Value, List_Name.本专科生离校系统},
                { re_id[4].Groups[1].Value, re_icon[4].Groups[1].Value, List_Name.雨课堂},
                { re_id[5].Groups[1].Value, re_icon[5].Groups[1].Value, List_Name.教务系统 },
                { re_id[6].Groups[1].Value, re_icon[6].Groups[1].Value, List_Name.研究生管理系统},
                { re_id[7].Groups[1].Value, re_icon[7].Groups[1].Value, List_Name.一卡通},
                { re_id[8].Groups[1].Value, re_icon[8].Groups[1].Value, List_Name.图书管理系统 },
                { re_id[9].Groups[1].Value, re_icon[9].Groups[1].Value, List_Name.课程中心},
                { re_id[10].Groups[1].Value, re_icon[10].Groups[1].Value, List_Name.信息门户 }
            };

            return List_Dic;

        }

    }
}
