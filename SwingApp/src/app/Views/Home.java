package app.Views;

import javax.swing.*;
import javax.swing.event.*;
import javax.swing.text.*;

import app.SwingApp;
import app.Annotations.AddComponent;
import app.Controllers.HomeController;

import java.lang.reflect.*;
import java.text.SimpleDateFormat;
import java.awt.*;
import java.awt.event.*;
import java.util.Date;
import java.util.concurrent.*;

/**
 * Home
 */
public class Home extends JFrame implements MouseListener {

	private HomeController homeController;

	private Boolean isExit = true;
	private Boolean isClicked = false;
	private String choiceNum = "";
	private ExecutorService threadHead = Executors.newSingleThreadExecutor();
	private ExecutorService threadPanel = Executors.newSingleThreadExecutor();

	private ImageIcon studentImage = new ImageIcon(
			Toolkit.getDefaultToolkit().getImage("src/app/Resources/student.png"));
	private ImageIcon teacherImage = new ImageIcon(
			Toolkit.getDefaultToolkit().getImage("src/app/Resources/teacher.png"));
	private ImageIcon backImage = new ImageIcon(
			Toolkit.getDefaultToolkit().getImage("src/app/Resources/backimage_deep.png"));

	private @AddComponent(-1) JLabel lableHead = new JLabel();

	private String[] buttonStrings = new String[] { "更换头像", "修改密码", "注销" };
	private JButton lineButton = new JButton("");

	private @AddComponent(-1) BackgroundPanel userPanel = new BackgroundPanel(backImage.getImage(),
			new FlowLayout(FlowLayout.CENTER, 10, 2));

	private @AddComponent(-1) JButton changeInformation = new JButton("修改学生信息");
	private @AddComponent(-1) JComboBox<String> studentBox = new JComboBox<>();
	private @AddComponent(-1) JPanel infoPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 5));
	private JButton addButton = new JButton("添加");

	private @AddComponent(-1) JButton communicationButton = new JButton("发送消息");
	private @AddComponent(-1) JPanel sendJPanel = new JPanel(null);
	private JTextPane historyArea = new JTextPane();
	private @AddComponent(1) JTextArea inputArea = new JTextArea();
	private @AddComponent(1) JScrollPane jsHistoryArea = new JScrollPane(historyArea);
	private @AddComponent(1) JButton sendButton = new JButton("发送");

	public Home(HomeController controller) {
		super();
		homeController = controller;
		homeController.listen();
		Init();
		AddEvent();
		receive();
	}

	private void Init() {
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setResizable(false);
		this.setSize(600, 400);
		this.setLocationRelativeTo(null);
		this.setLayout(null);
		this.setIconImage(Toolkit.getDefaultToolkit().getImage("src/app/Resources/home.png"));

		// 头像
		lableHead.setSize(64, 64);
		lableHead.setLocation(506, 5);
		if (SwingApp.isTeacher) {
			lableHead.setIcon(teacherImage);
		} else {
			lableHead.setIcon(studentImage);
		}

		// 空行
		lineButton.setPreferredSize(new Dimension(54, 12));
		lineButton.setContentAreaFilled(false);
		lineButton.setBorderPainted(false);
		lineButton.setEnabled(false);

		// 添加按钮到弹出panel
		userPanel.add(lineButton);
		for (String string : buttonStrings) {
			var temp = new JButton(string);
			temp.setName(string);
			temp.setSize(54, 25);
			temp.setBackground(Color.LIGHT_GRAY);
			temp.setMargin(new Insets(0, 0, 0, 0));
			if (string.equals(buttonStrings[2])) {
				temp.setMargin(new Insets(0, 12, 0, 12));
			}
			temp.addMouseListener(this);
			userPanel.add(temp);
		}

		userPanel.setSize(80, 90);
		userPanel.setLocation(500, 50);
		userPanel.setOpaque(false);
		userPanel.setVisible(false);


		
		historyArea.setEditable(false);
		jsHistoryArea.setSize(344, 204);
		jsHistoryArea.setLocation(3, 3);
		jsHistoryArea.setBorder(BorderFactory.createLineBorder(Color.BLACK));

		inputArea.setSize(344, 80);
		inputArea.setLocation(3, 210);
		inputArea.setBorder(BorderFactory.createLineBorder(Color.BLACK));

		sendButton.setSize(60, 26);
		sendButton.setLocation(287, 292);
		sendButton.setBackground(Color.LIGHT_GRAY);

		sendJPanel.setLocation(130, 20);
		sendJPanel.setSize(350, 320);
		sendJPanel.setBorder(BorderFactory.createLineBorder(Color.BLACK));


		if (SwingApp.isTeacher) {
			changeInformation.setSize(80, 25);
			changeInformation.setLocation(20, 100);
			changeInformation.setMargin(new Insets(0, 0, 0, 0));
			changeInformation.setBackground(Color.LIGHT_GRAY);

			communicationButton.setLocation(20, 200);
			communicationButton.setSize(80, 25);
			communicationButton.setMargin(new Insets(0, 0, 0, 0));
			communicationButton.setBackground(Color.LIGHT_GRAY);

			studentBox.setLocation(250, 30);
			studentBox.setSize(80, 30);
			studentBox.setVisible(false);

			infoPanel.setLocation(150, 90);
			infoPanel.setBorder(BorderFactory.createLineBorder(Color.BLACK));
			infoPanel.setVisible(false);

			addButton.addMouseListener(getInstence());

			sendJPanel.setVisible(false);

		} else {
			communicationButton.setVisible(false);

			sendJPanel.setVisible(true);
		}

		Class<?> types = this.getClass();
		for (Field field : types.getDeclaredFields()) {
			if (field.getAnnotation(AddComponent.class) != null) {
				try {
					switch (field.getAnnotation(AddComponent.class).value()) {
					case 1:
						sendJPanel.add((Component) field.get(this));
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
	}

	private void AddEvent() {

		lableHead.addMouseListener(new MouseInputAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				userPanel.setVisible(true);
				isClicked = true;
				super.mouseClicked(e);
			}

			@Override
			public void mouseExited(MouseEvent e) {
				isExit = true;
				if (isClicked) {
					threadHead.submit(() -> {
						try {
							Thread.sleep(1000 * 1);
							if (isExit) {
								userPanel.setVisible(false);
								isExit = false;
							}
						} catch (InterruptedException ex) {
							ex.printStackTrace();
						}

					});
				}
				isClicked = false;
				super.mouseExited(e);
			}
		});
		userPanel.addMouseListener(new MouseInputAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				isExit = false;
				super.mouseEntered(e);
			}

			@Override
			public void mouseExited(MouseEvent e) {
				isExit = true;
				threadPanel.submit(() -> {
					try {
						Thread.sleep(1000 * 1);
						if (isExit) {
							userPanel.setVisible(false);
							isExit = false;
						}
					} catch (InterruptedException ex) {
						ex.printStackTrace();
					}

				});
				super.mouseMoved(e);
			}
		});
		changeInformation.addMouseListener(new MouseInputAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				sendJPanel.setVisible(false);
				studentBox.removeAllItems();
				for (var kv : homeController.getStudent().entrySet()) {
					studentBox.addItem(kv.getKey());
				}
				studentBox.setVisible(true);

				super.mouseClicked(e);
			}
		});
		studentBox.addItemListener(new ItemListener() {
			@Override
			public void itemStateChanged(ItemEvent e) {
				switch (e.getStateChange()) {
				case ItemEvent.SELECTED:
					infoPanel.removeAll();
					// infoPanel.setLayout(new FlowLayout(FlowLayout.LEFT, 10, 5));
					for (var kv : homeController.getStudent().get(e.getItem()).entrySet()) {
						if (kv.getKey().equals("学号")) {
							choiceNum = kv.getValue();
						}
						var lable = new JLabel(kv.getKey() + ":");
						lable.setPreferredSize(new Dimension(45, 25));
						infoPanel.add(lable);

						var lablev = new JLabel(kv.getValue());
						lablev.setPreferredSize(new Dimension(100, 25));
						infoPanel.add(lablev);

						var change = new JButton("修改");
						change.setName("修改" + "_" + kv.getKey());
						change.setSize(55, 25);
						change.addMouseListener(getInstence());
						infoPanel.add(change);
						
						var del = new JButton("删除");
						del.setName("删除" + "_" + kv.getKey());
						del.setSize(55, 25);
						del.addMouseListener(getInstence());
						infoPanel.add(del);

					}
					infoPanel.setSize(320, (infoPanel.getComponentCount() / 4) * 25 + 4
							+ ((infoPanel.getComponentCount() / 4) + 1) * 6);

					addButton.setVisible(true);
					addButton.setName("添加");
					addButton.setSize(70, 25);
					addButton.setLocation(infoPanel.getLocation().x + (infoPanel.getSize().width - 113),
							infoPanel.getLocation().y + infoPanel.getSize().height + 5);

					add(addButton);

					infoPanel.setVisible(true);
					repaint();
					infoPanel.revalidate();
					break;

				case ItemEvent.DESELECTED:
					break;
				}
			}

		});

		communicationButton.addMouseListener(new MouseInputAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				studentBox.setVisible(false);
				infoPanel.setVisible(false);
				addButton.setVisible(false);
				sendJPanel.setVisible(true);

				super.mouseClicked(e);
			}
		});

		sendButton.addMouseListener(new MouseInputAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				String message = inputArea.getText();
				inputArea.setText("");
				if (message != null && !message.equals("")) {
					if(SwingApp.isTeacher){
						message="老师-"+SwingApp.name+":"+message+"\r\n";
					}else{
						message="学生-"+SwingApp.name+":"+message+"\r\n";
					}
					homeController.send(message);
					Date dNow = new Date();
					SimpleDateFormat ft = new SimpleDateFormat("yyyy.MM.dd - hh:mm:ss ");
					var doc = historyArea.getStyledDocument();
					SimpleAttributeSet timeSet = new SimpleAttributeSet();
					StyleConstants.setForeground(timeSet, Color.BLUE);
					StyleConstants.setFontSize(timeSet,10);
					SimpleAttributeSet messageSet = new SimpleAttributeSet();
					StyleConstants.setForeground(messageSet, Color.BLACK);
					StyleConstants.setFontSize(messageSet,14);

					try {
						doc.insertString(doc.getLength(), ft.format(dNow)+"\r\n", timeSet);

						doc.insertString(doc.getLength(), message, messageSet);

					} catch (BadLocationException e1) {
						e1.printStackTrace();
					}
				}else{
					JOptionPane.showMessageDialog(null, "消息不能为空", "提示", JOptionPane.PLAIN_MESSAGE);
				}

				super.mouseClicked(e);
			}
		});

	}


	private void receive() {
		new Thread(new Runnable(){
			@Override
			public void run() {
				while (true) {
					try {
					Thread.sleep(500);
					String message = homeController.receiveMessage();
					if (message != null) {
						Date dNow = new Date();
						SimpleDateFormat ft = new SimpleDateFormat("yyyy.MM.dd - hh:mm:ss ");
						var doc = historyArea.getStyledDocument();
						SimpleAttributeSet timeSet = new SimpleAttributeSet();
						StyleConstants.setForeground(timeSet, Color.BLUE);
						StyleConstants.setFontSize(timeSet, 10);
						SimpleAttributeSet messageSet = new SimpleAttributeSet();
						StyleConstants.setForeground(messageSet, Color.BLACK);
						StyleConstants.setFontSize(messageSet, 14);
							doc.insertString(doc.getLength(), ft.format(dNow) + "\r\n", timeSet);
							doc.insertString(doc.getLength(), message, messageSet);
					}
				} catch (Exception e1) {
						e1.printStackTrace();
					}
				}
			}
		}).start();

	}

	@Override
	public void mouseClicked(MouseEvent e) {
		isExit = true;
		userPanel.setVisible(false);
		if (e.getComponent().getName().equals(buttonStrings[0])) {
		} else if (e.getComponent().getName().equals(buttonStrings[1])) {
			String temp = JOptionPane.showInputDialog(null, "输入新密码", "修改密码", JOptionPane.PLAIN_MESSAGE);
			if (temp != null) {
				if (homeController.changePassword(temp)) {
					JOptionPane.showMessageDialog(null, "密码修改成功", "提示", JOptionPane.INFORMATION_MESSAGE);
				} else {
					JOptionPane.showMessageDialog(null, "密码修改失败", "提示", JOptionPane.ERROR_MESSAGE);
				}
			}
		} else if (e.getComponent().getName().equals(buttonStrings[2])) {
		} else if(e.getComponent().getName().equals("添加")){
			var tempPanel=new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 5));
			var lable=new JLabel("新属性名称:");
			lable.setPreferredSize(new Dimension(65, 25));
			
			var lablev=new JLabel("新属性的值:");
			lablev.setPreferredSize(new Dimension(65, 25));
			
			JTextField kField = new JTextField();
			kField.setPreferredSize(new Dimension(100, 25));


			JTextField vField = new JTextField();
			vField.setPreferredSize(new Dimension(100, 25));

			tempPanel.add(lable);
			tempPanel.add(kField);
			tempPanel.add(lablev);
			tempPanel.add(vField);
			tempPanel.setPreferredSize(new Dimension(100, 60));

			if(JOptionPane.showConfirmDialog(null, tempPanel, "添加", JOptionPane.OK_CANCEL_OPTION,JOptionPane.PLAIN_MESSAGE)==0){
				if (homeController.addItem(choiceNum,kField.getText(),vField.getText())) {
					JOptionPane.showMessageDialog(null, kField.getText()+"添加成功", "提示", JOptionPane.INFORMATION_MESSAGE);
				} else {
					JOptionPane.showMessageDialog(null, kField.getText()+"添加失败", "提示", JOptionPane.ERROR_MESSAGE);
				}
			}

		} else if (e.getComponent().getName().split("_")[0].equals("修改")) {
			String item= e.getComponent().getName().split("_")[1];
			String temp = JOptionPane.showInputDialog(null, "输入新"+item, "修改"+item, JOptionPane.PLAIN_MESSAGE);
			if (temp != null) {
				if (homeController.changeItem(choiceNum,item,temp)) {
					JOptionPane.showMessageDialog(null, item+"修改成功", "提示", JOptionPane.INFORMATION_MESSAGE);
				} else {
					JOptionPane.showMessageDialog(null, item+"修改失败", "提示", JOptionPane.ERROR_MESSAGE);
				}
			}
		} else if (e.getComponent().getName().split("_")[0].equals("删除")) {
			String item= e.getComponent().getName().split("_")[1];
			if(JOptionPane.showOptionDialog(null, "确认删除"+item, "删除"+item, JOptionPane.YES_NO_OPTION,JOptionPane.QUESTION_MESSAGE, null, new String[]{"确定","取消"}, null)==0){
				if (homeController.delItem(choiceNum,item)) {
					JOptionPane.showMessageDialog(null, item+"删除成功", "提示", JOptionPane.INFORMATION_MESSAGE);
				} else {
					JOptionPane.showMessageDialog(null, item+"删除失败", "提示", JOptionPane.ERROR_MESSAGE);
				}
			}
		}

	}

	@Override
	public void mousePressed(MouseEvent e) {
	}

	@Override
	public void mouseReleased(MouseEvent e) {
	}

	@Override
	public void mouseEntered(MouseEvent e) {
		isExit = false;
	}

	@Override
	public void mouseExited(MouseEvent e) {
	}

	public MouseListener getInstence(){
		return this;
	}

	public class BackgroundPanel extends JPanel {

		private Image image = null;

		public BackgroundPanel(Image image, LayoutManager layout) {
			super(layout);
			this.image = image;
		}

		protected void paintComponent(Graphics g) {
			super.paintComponent(g);
			g.drawImage(image, 0, 0, this.getWidth(), this.getHeight(), this);
		}
	}

}