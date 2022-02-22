using System;
using System.Collections.Generic;
using System.Text;

namespace dotnet_core
{
    /// <summary>
    /// 统一门户App名称
    /// </summary>
    public enum List_Name
    {
        正版软件 = 0,
        安心付 = 1,
        学工系统 = 2,
        本专科生离校系统 = 3,
        雨课堂 = 4,
        教务系统 = 5,
        研究生管理系统 = 6,
        一卡通 = 7,
        图书管理系统 = 8,
        课程中心 = 9,
        信息门户 = 10
    }

    /// <summary>
    /// 一卡通信息
    /// </summary>
    public enum Card
    {
        学号 = 0,
        卡状态 = 1,
        姓名 = 2,
        主钱包余额 = 3,
        性别 = 4,
        补助余额 = 5,
        身份 = 6,
        单位 = 7
    }

    /// <summary>
    /// 统一门户应用合集（含.icon）
    /// </summary>
    public class Dic:Dictionary<List_Name,List<string>>
    {


        public void Add(string Id,string icon,List_Name name)
        {
            List<string> l = new List<string>
            {
                Id,icon
            };
            base.Add(name,l);
        }
    }
}
