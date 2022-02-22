using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;

namespace dotnet_core
{
    public class EductionSystem
    {
        private const string Base_Url = "http://202.203.158.158/app/forward.action?id=";
        private const string Url_Class = "http://202.203.158.106/jwweb/znpk/Pri_StuSel.aspx";
        private const string Url_Src= "http://202.203.158.106/jwweb/znpk/Pri_StuSel_rpt.aspx?m=";
        private const string Url_Img= "http://202.203.158.106/jwweb/znpk/";


        private readonly CookieContainer cookieContainer;

        /// <summary>
        /// 教务系统
        /// </summary>
        /// <param name="list">App列表</param>
        /// <param name="container">Cookies集合</param>

        public EductionSystem(Dic list,CookieContainer container)
        {
            HttpWebRequest Get_Url = WebRequest.CreateHttp(Base_Url + list[List_Name.教务系统][0]);
            Get_Url.ContentType = Login.Content_Type;
            Get_Url.CookieContainer = container;

            string Url = new StreamReader(Get_Url.GetResponse().GetResponseStream()).ReadToEnd();
            Match Re_url= Regex.Match(Url, @"location.href=""(.*?)"";");

            HttpWebRequest Get_Cookies = WebRequest.CreateHttp(Re_url.Groups[1].Value);
            Get_Cookies.ContentType = Login.Content_Type;
            Get_Cookies.CookieContainer = container;
            

            HttpWebResponse response = (HttpWebResponse)Get_Cookies.GetResponse();

            cookieContainer = container;
        }

        /// <summary>
        /// 长度为十五的随机字符串
        /// </summary>
        /// <returns></returns>
        private string GetRandomString()
        {
            Random random = new Random();
            string result_List = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            string result = "";
            for (int i = 0; i < 15; i++)
            {
                result+= result_List[random.Next(result_List.Length)];
            }

            return result;
        }
        /// <summary>
        /// 获取课程列表
        /// </summary>
        /// <param name="Year">要获取的年份以及学期</param>
        public void GetClassList(int Year)
        {
            HttpWebRequest Get_Url = WebRequest.CreateHttp(Url_Class);
            Get_Url.ContentType = Login.Content_Type;
            Get_Url.CookieContainer = cookieContainer;

            MatchCollection RR = Regex.Matches(new StreamReader(Get_Url.GetResponse().GetResponseStream()).ReadToEnd(), @"value=""(.*?)""");
            
            string RandomString= this.GetRandomString();

            Encryption encryption = new Encryption();

            string Data_Md5 = encryption.GetMd5(1,RandomString);

            string data =  "Sel_XNXQ" + "=" + Year + "&" + 
                "rad" + "=" + 0 + "&" + 
                "px" + "=" + 0 + "&" + 
                "txt_yzm" + "&" + "" + "&" + 
                "hidyzm" + "=" + RR[6].Groups[1].Value + "&" + 
                "hidsjyzm" + "=" + Data_Md5;


            HttpWebRequest Get_ClassSrc = WebRequest.CreateHttp(Url_Src+RandomString);
            Get_ClassSrc.Method = "POST";
            Get_ClassSrc.ContentType = Login.Content_Type;
            Get_ClassSrc.CookieContainer = cookieContainer;

            using (Stream stream= Get_ClassSrc.GetRequestStream())
            {
                stream.Write(Encoding.Default.GetBytes(data), 0, data.Length);
            }

            HttpWebResponse response_src = (HttpWebResponse)Get_ClassSrc.GetResponse();        

            Match R_re = Regex.Match(new StreamReader(response_src.GetResponseStream()).ReadToEnd(), @"src='(.*?)'");

            HttpWebRequest Get_Img = WebRequest.CreateHttp(Url_Img + R_re.Groups[1].Value);
            Get_Img.CookieContainer = cookieContainer;

            HttpWebResponse Response = (HttpWebResponse)Get_Img.GetResponse();
            long len = Response.ContentLength;
            byte[] b = new byte[len];

            using (Stream stream= Response.GetResponseStream())
            {
                stream.Read(b,0,Convert.ToInt32(len));
                encryption.Get_Class(b);
            }


        }
    } 
}
