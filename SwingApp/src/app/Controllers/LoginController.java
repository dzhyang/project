package app.Controllers;

import java.util.Map;

import app.SwingApp;
import app.Models.SqlHelp;

/**
 * LoginController
 */
public class LoginController {
    
    public boolean IsLoginSucess(String username,String password,boolean isTeacher){
        SqlHelp sqlHelp=new SqlHelp();
        try {
            if(isTeacher){
                if (sqlHelp.select("teacher",username,"密码").equals(password)) {
                    SwingApp.username=username;
                    SwingApp.isTeacher=isTeacher;
                    SwingApp.name=sqlHelp.select("teacher",username,"姓名");
                    return true;
                }else{
                    return false;
                }
            }else{
                if (sqlHelp.select("student",username,"密码").equals(password)) {
                    SwingApp.username = username;
                    SwingApp.isTeacher=isTeacher;    
                    SwingApp.name=sqlHelp.select("student",username,"姓名");
                    return true;
                }else{
                    return false;
                }
            }
        } catch (Exception e) {
            return false;
        }

    }
    
}