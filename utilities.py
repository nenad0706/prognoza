
w_img = ["☀️ ","🌦️ ","🌤️ ","🌦️ ","⛅","🌦️ ","☁️ ","🌧️ "]
blk = 30
red = 31
grn = 32
ylw = 33
blu = 34
prp = 35
cyn = 36
wht = 37

# returns emoji based on rain and cloud percentage
def form_image(rain, clouds):
	global w_img
	if clouds == 100:
		clouds = 99
	w_img_index = (clouds // 25) * 2
	if rain > 50:
		w_img_index += 1
	return " " + w_img[w_img_index] + "  "

# return colored text based on rain percentage
def color_rain(text):
	texttemp = text[0:text.index("%")]
	inttemp = int(texttemp, 10)
	if inttemp < 25:
		return cl(text, blk, wht+60, 0)
	elif inttemp < 50:
		return cl(text, blk, cyn+60, 0)
	elif inttemp < 75:
		return cl(text, blk, blu+60, 0)
	else:
		return cl(text, wht, blu, 0)

# return colored text based on temperature
def color_temp(text):
	texttemp = text[0:text.index("°")]
	inttemp = int(texttemp, 10)
	if inttemp < -5:
		return cl(text, blk, blu+60, 0)
	elif inttemp < 5:
		return cl(text, blk, wht+60, 0)
	elif inttemp < 15:
		return cl(text, blk, ylw+60, 0)
	elif inttemp < 25:
		return cl(text, blk, grn+60, 0)
	elif inttemp < 35:
		return cl(text, blk, yellow, 0)
	else:
		return cl(text, wht, red, 1)

# return colored text
def cl(text, foreground, background, style):
	colored = "\033[" + str(style) + ";"+ str(foreground)
	if background != 0:
		colored += ";" + str(background + 10)
	colored += "m" + text + "\033[0m"
	return colored

# fills blank space $number times, no line break
def fill(number):
	s = "{0:<" + str(number) + "}"
	print(s.format(" "), end="")