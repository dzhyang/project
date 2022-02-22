package app.Controllers;

import app.SwingApp;
import app.Models.SqlHelp;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;

/**
 * HomeController
 */
public class HomeController {


    public void changeHead() {

    }

    public boolean changePassword(String newst) {
        SqlHelp sqlHelp = new SqlHelp();
        try {
            if (SwingApp.isTeacher) {
                sqlHelp.updata("teacher", SwingApp.username, "密码", newst);
            } else {
                sqlHelp.updata("student", SwingApp.username, "密码", newst);
            }
            return true;
        } catch (Exception e) {
            return false;
        } finally {
            sqlHelp.close();
        }
    }

    public void exitSystem() {

    }

    public Map<String, HashMap<String, String>> getStudent() {
        Map<String, HashMap<String, String>> studentsMap = new HashMap<>();
        SqlHelp sqlHelp = new SqlHelp();
        for (var num : sqlHelp.select("student").entrySet()) {
            HashMap<String, String> temp = new HashMap<>();
            temp.put("学号", num.getKey());
            for (var kv : num.getValue().entrySet()) {
                if (kv.getKey().equals("姓名")) {
                    studentsMap.put(kv.getValue(), temp);
                } else {
                    temp.put(kv.getKey(), kv.getValue());
                }
            }
        }
		sqlHelp.close();
        return studentsMap;
    }

    public boolean changeItem(String Num, String item, String newst) {
        SqlHelp sqlHelp = new SqlHelp();
        try {
            sqlHelp.updata("student", Num, item, newst);
            return true;
        } catch (Exception e) {
            return false;
        } finally {
            sqlHelp.close();
        }
    }

    public boolean delItem(String Num, String item) {
        SqlHelp sqlHelp = new SqlHelp();
        try {
            sqlHelp.del("student", Num, item);
            return true;
        } catch (Exception e) {
            return false;
        } finally {
            sqlHelp.close();
        }
    }

    public boolean addItem(String Num, String item, String st) {
        SqlHelp sqlHelp = new SqlHelp();
        try {
            sqlHelp.insert("student", Num, item, st);
            return true;
        } catch (Exception e) {
            return false;
        } finally {
            sqlHelp.close();
        }
    }


    private Socket socket=null;
    private ServerSocket sockerServer=null;
    private Socket sockerClient=null;;

    public void listen() {
        new Thread(new Runnable(){
            @Override
            public void run() {
                while (true) {
                    try {
                        if (sockerServer==null) {
							sockerServer = new ServerSocket(SwingApp.isTeacher ? 52000 : 52100);
                        }
                        socket=sockerServer.accept();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                
            }
        }).start();

    }

    public void send(String message) {
        try {
            if (sockerClient==null) {
                sockerClient=new Socket("127.0.0.1",SwingApp.isTeacher ? 52100 : 52000);
            }
            var writer=sockerClient.getOutputStream();
            writer.write(message.getBytes("UTF-8"));
            writer.flush();
            writer.close();
            sockerClient.close();
            sockerClient=null;
        } catch (IOException e) {
            e.printStackTrace();
        }
        

	}

	public String receiveMessage() {
        try {
            //System.out.println(socket.getPort());
            if(socket!=null){
				var bytes = socket.getInputStream().readAllBytes();
                socket.close();
                socket=null;
                return new String(bytes, 0, bytes.length);
            }
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
        return null;

	}
}