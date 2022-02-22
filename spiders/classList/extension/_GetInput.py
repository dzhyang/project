import msvcrt
def GetInput():
	uer = input("输入学号：")
	print('输入密码: ', end='', flush=True)
	li = []
	while 1:
		ch = msvcrt.getch()
		#回车
		if ch == b'\r':
			msvcrt.putch(b'\n')
			psw=b''.join(li).decode()
			break
		#退格
		elif ch == b'\x08':
			if li:
				li.pop()
				msvcrt.putch(b'\b')
				msvcrt.putch(b' ')
				msvcrt.putch(b'\b')
		else:
			li.append(ch)
			msvcrt.putch(b'*')
	return uer,psw