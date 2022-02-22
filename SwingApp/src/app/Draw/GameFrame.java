package app.Draw;

import java.awt.Color;
import java.awt.Font;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Toolkit;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.ImageIcon;
 
public class GameFrame extends Frame {
 
	private ImageIcon studentImage = new ImageIcon(Toolkit.getDefaultToolkit().getImage("src/app/Resources/student.png"));
 
	public void launchFrame() {
		//设置窗口大小和位置
		setSize(500, 500);
		setLocation(100, 100);
		//将窗口设置为可见
		setVisible(true);
 
		//启动线程
		new PaintThread().start();
 

		addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
	}
 
	private double x = 100, y = 100;
 

	@Override
	public void paint(Graphics g) {
		//画线
		g.drawLine(100, 100, 200, 200);
		//画矩形
		g.drawRect(100, 100, 200, 200);
		//画空心椭圆
		g.drawOval(100, 100, 200, 200);
		//设置字体
		g.setFont(new Font("宋体", Font.BOLD, 30));
		//绘制文字
		g.drawString("第一次画图", 200, 200);
		//画实心矩形
		g.fillRect(100, 100, 20, 20);
		//保存画笔颜色
		Color c = g.getColor();
		//设置画笔颜色
		g.setColor(Color.GREEN);
		//画实心矩形
		g.fillOval(300, 300, 20, 20);
		//重设画笔颜色
		g.setColor(c);
		//绘制图片
		g.drawImage(studentImage.getImage(), (int) x, (int) y, null);
		//更改图片坐标
		x += 3;
		y += 3;

	}
 
	//实现多线程类
	class PaintThread extends Thread {
 
		public void run() {
			while (true) {
				//重绘窗口
				repaint();
				try {
					//暂停四十毫秒
					Thread.sleep(40);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}
 
	}
 
	public static void main(String[] args) {
		GameFrame gf = new GameFrame();
		gf.launchFrame();
	}
 
}

