package app;

import app.Controllers.HomeController;
import app.Controllers.LoginController;
import app.Views.*;

/**
 * swingapp main class
 */
public class SwingApp {
    public static String name;
    public static boolean isTeacher;
    public static String username;

    public static void main(String[] args) {

        LoginController loginController = new LoginController();
        Login login = new Login(loginController);
        login.showDialog();
        if(!login.getIsSucess())
        {
            System.exit(0);
        }
        Home home=new Home(new HomeController());
        home.setVisible(true);
    }
}
