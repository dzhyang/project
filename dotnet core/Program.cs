using System;
using System.Collections.Generic;
using System.Net;
namespace dotnet_core
{
    class Program
    {
        public static void Main(string[] args)
        {

            //登录Cookies，主页信息集合
            Login login = new Login("201713454106", "*********");
            CookieContainer cook= login.GetCookies();
            Dic List_Get= login.GetList(cook);


            //一卡通信息集合
            //GetCardMsg msg = new GetCardMsg();
            //Dictionary<Card,string> Card_Msg= msg.GetMsg(List_Get,cook);
            EductionSystem eductionSystem = new EductionSystem(List_Get, cook);


            eductionSystem.GetClassList(20181);

            Console.ReadKey();
        }
    }
}
