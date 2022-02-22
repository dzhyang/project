package app.Views;

import java.awt.*;
import java.awt.event.*;
import java.lang.reflect.*;
import javax.swing.*;
import javax.swing.event.*;

import app.Annotations.AddComponent;
import app.Controllers.LoginController;

public class Login extends JDialog {
    private LoginController loginController;

    private boolean isTeacher = false;
    private boolean isSucess = false;
    private int loginCount = 0;
    private boolean isShowValidCode = false;

    private ImageIcon studentImage = new ImageIcon(Toolkit.getDefaultToolkit().getImage("src/app/Resources/student.png"));
    private ImageIcon teacherImage = new ImageIcon(Toolkit.getDefaultToolkit().getImage("src/app/Resources/teacher.png"));
    private ImageIcon validCodeImage = new ImageIcon(Toolkit.getDefaultToolkit().getImage("src/app/Resources/ValidCode.gif"));
    private Image loginImage = Toolkit.getDefaultToolkit().getImage("src/app/Resources/Login.png");

    private @AddComponent(1) JTextField userName = new JTextField();
    private @AddComponent(1) JPasswordField passWord = new JPasswordField();
    private @AddComponent(1) JLabel lableUserName = new JLabel("账号");
    private @AddComponent(1) JLabel lablePassWord = new JLabel("密码");
    // private @AddComponent(-1) JComboBox<String> listComboBox=new JComboBox<>(new
    // String[]{"学生","教师"});
    private @AddComponent(1) Lable labelImage = new Lable(studentImage);
    private @AddComponent(-1) JPanel inputPanel = new JPanel(null);

    private @AddComponent(2) JLabel lableValidCodeText = new JLabel("验证码");
    private @AddComponent(2) JLabel lableValidCodeImage = new JLabel(validCodeImage);
    private @AddComponent(2) JTextField validCodeInput = new JTextField();
    private @AddComponent(-2) JPanel validCodePanel = new JPanel(null);

    private @AddComponent(3) JButton buttonLogin = new JButton("登录");
    private @AddComponent(-3) JPanel buttoPanel = new JPanel(null);

    public Login(LoginController controller) {
        super();
        loginController=controller;
        Init();
        AddEvent();
    }

    /**
     * 初始化UI界面
     */
    private void Init() {
        this.setBounds(0, 0, 400, 250);
        this.setResizable(false);
        this.setIconImage(loginImage);
        this.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        this.setLocationRelativeTo(null);
        this.setLayout(null);

        // #region 用户名 密码 身份
        lableUserName.setSize(30, 20);
        lableUserName.setLocation(75, 5);
        lableUserName.setFont(new Font("微软雅黑", Font.PLAIN, 14));

        userName.setSize(140, 30);
        userName.setLocation(lableUserName.getLocation().x + lableUserName.getSize().width + 10, 0);
        userName.setFont(new Font("微软雅黑", Font.PLAIN, 16));

        // 密码
        lablePassWord.setSize(30, 20);
        lablePassWord.setLocation(75, 45);
        lablePassWord.setFont(new Font("微软雅黑", Font.PLAIN, 14));

        passWord.setSize(140, 30);
        passWord.setLocation(lablePassWord.getLocation().x + lablePassWord.getSize().width + 10, 40);
        passWord.setFont(new Font("微软雅黑", Font.PLAIN, 16));

        // 身份
        // listComboBox.setSize(60, 30);
        // listComboBox.setLocation(0, 0);
        // listComboBox.setBackground(Color.WHITE);
        // listComboBox.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        labelImage.setBounds(0, 3, 64, 64);
        labelImage.setToolTipText("点击切换为教师登录");

        // 账号密码及身份容器
        inputPanel.setSize(passWord.getLocation().x + passWord.getSize().width,passWord.getLocation().y + passWord.getSize().height);
        inputPanel.setLocation(this.getWidth() / 2 - inputPanel.getWidth() / 2, (this.getHeight() * 3) / 20);

        // #endregion

        // region 验证码
        lableValidCodeText.setSize(45, 20);
        lableValidCodeText.setLocation(0, 1);
        lableValidCodeText.setFont(new Font("微软雅黑", Font.PLAIN, 14));

        validCodeInput.setSize(50, 28);
        validCodeInput.setLocation(lableValidCodeText.getLocation().x + validCodeInput.getSize().width + 10, 0);
        validCodeInput.setFont(new Font("微软雅黑", Font.PLAIN, 16));

        lableValidCodeImage.setSize(60, 20);
        lableValidCodeImage.setLocation(validCodeInput.getLocation().x + validCodeInput.getSize().width + 10, 1);

        validCodePanel.setVisible(false);
        validCodePanel.setSize(lableValidCodeImage.getLocation().x + lableValidCodeImage.getSize().width,validCodeInput.getLocation().y + validCodeInput.getSize().height);
        validCodePanel.setLocation(this.getWidth() / 2 - validCodePanel.getWidth() / 2 + 10,inputPanel.getLocation().y + inputPanel.getSize().height + 10);
        // #endregion

        // #region 按钮
        buttonLogin.setSize(75, 25);
        buttonLogin.setLocation(0, 0);
        buttonLogin.setFont(new Font("微软雅黑", Font.PLAIN, 16));
        buttonLogin.setBackground(Color.LIGHT_GRAY);
        // 容器
        buttoPanel.setSize(75, 25);
        buttoPanel.setLocation(this.getWidth() / 2 - buttoPanel.getWidth() / 2,
                validCodePanel.getLocation().y + validCodePanel.getSize().height + 15);

        // #endregion

        // #region 添加组件到对应容器

        Class<?> type = this.getClass();
        for (Field field : type.getDeclaredFields()) {
            if (field.getAnnotation(AddComponent.class) != null) {
                try {
                    switch (field.getAnnotation(AddComponent.class).value()) {
                    case 1:
                        inputPanel.add((Component) field.get(this));
                        break;
                    case 2:
                        validCodePanel.add((Component) field.get(this));
                        break;
                    case 3:
                        buttoPanel.add((Component) field.get(this));
                        break;
                    default:
                        this.add((Component) field.get(this));
                        break;
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
        // #endregion

    }

    /**
     * 添加事件监听
     */
    private void AddEvent() {
        // 登录身份切换
        labelImage.addMouseListener(new MouseInputAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (isTeacher) {
                    labelImage.setIcon(studentImage);
                    labelImage.setToolTipText("点击切换为教师登录");
                    isTeacher = false;
                } else {
                    labelImage.setIcon(teacherImage);
                    labelImage.setToolTipText("点击切换为学生登录");
                    isTeacher = true;
                }
                super.mouseClicked(e);
            }
        });
        
        // 判断登录是否成功
        buttonLogin.addMouseListener(new MouseInputAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (userName.getText().equals("")) {
                    JOptionPane.showMessageDialog(null, "用户名为空", "错误", JOptionPane.ERROR_MESSAGE);
                } else if (String.valueOf(passWord.getPassword()).equals("")) {
                    JOptionPane.showMessageDialog(null, "密码为空", "错误", JOptionPane.ERROR_MESSAGE);
                } else if (validCodeInput.getText().equals("") && isShowValidCode) {
                    JOptionPane.showMessageDialog(null, "验证码为空", "错误", JOptionPane.ERROR_MESSAGE);
                } else if (!validCodeInput.getText().equals("kdgh") && isShowValidCode) {
                    JOptionPane.showMessageDialog(null, "验证码错误", "错误", JOptionPane.ERROR_MESSAGE);
                } else if (!loginController.IsLoginSucess(userName.getText(), String.valueOf(passWord.getPassword()),isTeacher)) {
                    JOptionPane.showMessageDialog(null, "账号/密码错误", "错误", JOptionPane.ERROR_MESSAGE);
                } else {
                    isSucess = true;
                    Close();
                    return;
                }
                if (loginCount > 2) {
                    validCodePanel.setVisible(true);
                    isShowValidCode = true;
                } else {
                    loginCount += 1;
                }
                super.mouseClicked(e);
            }
        });

    }

    // 获取是否登录成功
    public boolean getIsSucess() {
        return isSucess;
    }



    // 模态显示窗口
    public void showDialog() {
        this.setModal(true);
        this.setVisible(true);
    }

    // 关闭窗口
    private void Close() {
        this.dispose();
    }

    public class Lable extends JLabel {

        public Lable(ImageIcon studentImage) {
            super(studentImage);
        }

        @Override
        public JToolTip createToolTip() {
            JToolTip jt = super.createToolTip();
            jt.setBackground(Color.WHITE);
            jt.updateUI();
            return jt;
        }
        
        
    }
}