using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace dotnet_core
{
    public class Encryption
    { 
        private Socket socket;
        private Socket socket_IMG;

        public Encryption()
        {
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            
            socket_IMG = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            
        }


        public  string GetMd5(int id,string str)
        {
            socket.Connect(new IPEndPoint(IPAddress.Parse("172.16.43.16"), 520));
            socket.Send(Encoding.Default.GetBytes(@"{""id"":"+@""""+id+@""""+@",""value"":" +@""""+str+@"""" +"}"));
            byte[] b=new byte[1024];
            int len=socket.Receive(b);
            socket.Close();
            return Encoding.Default.GetString(b,0,len);
        }
        public void Get_Class(byte[] b)
        {
            
            socket_IMG.Connect(new IPEndPoint(IPAddress.Parse("172.16.43.16"), 521));
            socket_IMG.Send(b);
            byte[] r = new byte[1024];
            int len = socket_IMG.Receive(r);
            Console.WriteLine(Encoding.Default.GetString(r,0,len));
            socket_IMG.Close();

            //return Encoding.Default.GetString(b, 0, len);
        }
    }
}
