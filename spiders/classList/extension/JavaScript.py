import execjs
def JS(URI,function,string):
	with open(URI, "r", encoding="UTF-8") as encryption:
		line = encryption.readline()
		html_str = ''
		while line:
			html_str = html_str + line
			line = encryption.readline()
	PW_JS = execjs.compile(html_str)
	PW_value = PW_JS.call(function, string)
	return PW_value