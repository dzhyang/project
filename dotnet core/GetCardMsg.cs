using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;


namespace dotnet_core
{
    public class GetCardMsg
    {
        private const string Base_Url = "http://202.203.158.158/app/forward.action?id=";
        private const string Url_Get_msg = "http://10.90.2.8/selfsearch/User/Home.aspx";


        /// <summary>
        /// 获取一卡通信息
        /// </summary>
        /// <param name="DC">统一门户App信息合集</param>
        /// <param name="container">请求所需Cookies</param>
        /// <returns>返回一卡通信息集合</returns>
        public Dictionary<Card,string> GetMsg(Dic DC,CookieContainer container)
        {
            //登录一卡通页面
            HttpWebRequest Get_Url_1 = WebRequest.CreateHttp(Base_Url + DC[List_Name.一卡通][0]);
            Get_Url_1.ContentType = Login.Content_Type;
            Get_Url_1.CookieContainer = container;

            HttpWebResponse Response_1 =(HttpWebResponse)Get_Url_1.GetResponse();



            string Url_1=new StreamReader(Response_1.GetResponseStream()).ReadToEnd();
            Match re_Url_1= Regex.Match(Url_1, @"location.href=""(.*?)"";");

            HttpWebRequest Get_Url_2 = WebRequest.CreateHttp(re_Url_1.Groups[1].Value);
            Get_Url_2.ContentType = Login.Content_Type;
            Get_Url_2.CookieContainer = container;

            HttpWebResponse Response_2 = (HttpWebResponse)Get_Url_2.GetResponse();
            string Url_2=new StreamReader(Response_2.GetResponseStream()).ReadToEnd();




        
            Match re_Url_2 = Regex.Match(Url_2, @"action='(.*?)'");
            MatchCollection re_Value = Regex.Matches(Url_2, @"value='(.*?)'");
            string data = "username" + "=" + re_Value[0].Groups[1].Value + "&" + "timestamp" + "=" + re_Value[1].Groups[1].Value + "&" + "auid" + "=" + re_Value[2].Groups[1].Value;

            HttpWebRequest Get_Cookies = WebRequest.CreateHttp(re_Url_2.Groups[1].Value);
            Get_Cookies.ContentType = Login.Content_Type;
            Get_Cookies.CookieContainer = container;
            Get_Cookies.Method = "POST";

            using (Stream stream= Get_Cookies.GetRequestStream())
            {
                stream.Write(Encoding.Default.GetBytes(data), 0, data.Length);
            }

            HttpWebResponse Response_3 = (HttpWebResponse)Get_Cookies.GetResponse();





            //获取一卡通信息
            HttpWebRequest Get_Msg = WebRequest.CreateHttp(Url_Get_msg);
            Get_Msg.ContentType = Login.Content_Type;
            Get_Msg.CookieContainer = container;

            HttpWebResponse Response_Msg = (HttpWebResponse)Get_Msg.GetResponse();

            MatchCollection Result= Regex.Matches(new StreamReader(Response_Msg.GetResponseStream()).ReadToEnd(), @"<span>(.*?)：(.*?)</span>");

            Dictionary<Card, string> Card_Dic = new Dictionary<Card, string>()
            {
                { Card.学号,Result[0].Groups[2].Value},
                { Card.卡状态,Result[1].Groups[2].Value},
                { Card.姓名,Result[2].Groups[2].Value},
                { Card.主钱包余额,Result[3].Groups[2].Value},
                { Card.性别,Result[4].Groups[2].Value},
                { Card.补助余额,Result[5].Groups[2].Value},
                { Card.身份,Result[6].Groups[2].Value},
                { Card.单位,Result[7].Groups[2].Value},
                
            };
            return Card_Dic;
        }
    }
}
