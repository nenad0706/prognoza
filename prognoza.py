#!/home/nenad/dev/scripts/prognoza/env/bin/python
# -*- coding: UTF-8 -*-

import bs4 as bs
import requests
from utilities import *


next_url = "https://www.accuweather.com/sr/rs/belgrade/298198/hourly-weather-forecast/298198"

generaldata = {"location":"Beograd, Srbija"}
hourlydata = {
	"images" :  "",
	"hours"  :  "      ",
	"temp" :	" Temp ",
	"rain" : 	" Rain "
}
dayslist = []
rainlist = []
cloudslist = []

left_indent = "    "
got_daily = False

def get_weather_hourly():

	global hourlydata, got_daily, next_url
	global rainlist, cloudslist
	global dayslist	

	# scrape web
	headers = {'User-Agent':'Mozilla/5.0'}
	page = requests.get(next_url, headers=headers)
	soup = bs.BeautifulSoup(page.text, 'lxml')

	# scrape downloaded page (for development)
	#page = open("tempdata4dev/page.html", "r").read()
	#soup = bs.BeautifulSoup(page, 'lxml')
	
	if not got_daily:

		# get general data
		nowfeed = soup.select("div#feed-tabs")[0].select("ul li")[0]
		generaldata["now-temp"] = nowfeed.select("div div.info div.temp span.large-temp")[0].text
		generaldata["now-feel"] = nowfeed.select("div div.info div.temp span.real-feel")[0].text

		# get 5 days data
		daysfeed = soup.select("div#feed-tabs")[1]
		lis = daysfeed.select("ul li")
		for li in lis:
			day = li.find()
			daydata = {}
			daydata["title"] = day.select("h3")[0].text.upper()
			daydata["date"] = day.find("h4").text
			
			daydata["infodescr"] = day.select("div.info span.cond")[0].text

			daydata["infotemp"] = ""
			dayinfo = day.select("div.info div.temp")[0].text.split()
			for info in dayinfo:
				if info != "C":
					daydata["infotemp"] += info

			dayslist.append(daydata)

		got_daily = True
	
	next_url = soup.select("div#detail-hourly div.clearfix div.control-bar.hourly-control a.right-float")[0]['href']
	# DIV RAIN
	tempsati = soup.select("div.hourly-table.precip-hourly table thead tr td")
	for sat in tempsati[0::2]:
		hours_val = int(sat.select("div")[0].text, 10)
		hours_str = " {0:<4}".format(sat.select("div")[0].text)
		if 7 <= hours_val <= 20:
			hourlydata["hours"] += cl(hours_str, wht, blk, 0)
		else:
			hourlydata["hours"] += cl(hours_str, cyn, blk, 0)

	tempsati = soup.select("div.hourly-table.precip-hourly table tbody tr td")
	for sat in tempsati[0:8][0::2]:
		rain_val = sat.select("span")[0].text
		hourlydata["rain"] += color_rain(" {0:<4}".format(rain_val))
		rainlist.append(int(rain_val[:-1], 10))

	# DIV TEMPERATURE
	tempsati = soup.select("div.hourly-table.overview-hourly table tbody tr td")
	for sat in tempsati[0:8][0::2]:
		hourlydata["temp"] += color_temp(" {0:<4}".format(sat.select("span")[0].text))

	# DIV SKY
	tempsati = soup.select("div.hourly-table.sky-hourly table tbody tr td")
	for sat in tempsati[8:15][0::2]:
		clouds_val = sat.select("span")[0].text
		cloudslist.append(int(clouds_val[:-1], 10))


def form_images_hourly():
	global rainlist, cloudslist, hourlydata

	for i in range(len(rainlist)):
		hourlydata["images"] += form_image(rainlist[i], cloudslist[i]) 

'''
	prints left table 
'''
def fill_or_print_general(current_line):
	bgc = blk
	fgc = wht
	st = 1
	startline = 2
	global generaldata
	# print first row
	if current_line == 1:
		print(left_indent + cl("{0:<15}".format("Ｐ Ｒ Ｏ Ｇ Ｎ Ｏ Ｚ Ａ"), fgc, 0, 1), end="")
		fill(4)
	elif current_line - startline == 1:
		print(left_indent + cl("{0:<23}".format(""), fgc, bgc, 0), end="")
		fill(4)
	elif current_line - startline == 2:
		print(left_indent + cl("    ", fgc, bgc, st), end="")
		print(cl("{0:<19}".format(generaldata["now-temp"]), fgc, bgc, st), end="")
		fill(4)
	elif current_line - startline == 3:
		print(left_indent + cl("    ", fgc, bgc, st), end="")
		print(cl("{0:<19}".format(generaldata["location"]), fgc, bgc, st), end="")
		fill(4)
	elif current_line - startline == 4:
		print(left_indent + cl("    ", fgc, bgc, st), end="")
		print(cl("{0:<19}".format(generaldata["now-feel"]), fgc, bgc, 0), end="")
		fill(4)
	elif current_line - startline == 5:
		print(left_indent + cl("{0:<23}".format(""), fgc, bgc, 0), end="")
		fill(4)
	else :
		fill(len(left_indent) + 27)	

# =========================================================== SCRAPE

get_weather_hourly()
get_weather_hourly()
get_weather_hourly()
form_images_hourly()

# =========================================================== PRINT


print()

# used for printing general data on the left side
# tracks current line number as some cells in right
# table may extend to 3 lines
tline = 1
for k in range(1, 5):

	# define color
	if k % 2 != 0:
		d_bg = blk+60 	# day header background
		d_fg = wht		# day header foreground
		d_s = 1			# day header style
	else:
		d_bg = blk
		d_fg = wht
		d_s = 1

	# FIRST ROW
	fill_or_print_general(tline)
	print(
		cl(" {0:<28}".format("{0:<3}, {1}".format(dayslist[k]["title"], dayslist[k]["date"])), d_fg, d_bg, 1),
		end=""
		)
	print(cl( dayslist[k]["infotemp"].rjust(10), d_fg, d_bg, 1))
	tline += 1

	# SECOND ROW (and maybe 3rd)
	fill_or_print_general(tline)
	# if description is more than 28 characters, break new line
	newline = False
	descr = dayslist[k]["infodescr"]
	if len(descr) < 29:
		print(cl(" {0:<38}".format(descr), d_fg, d_bg, 0))
		tline += 1
	else:
		newline = True
		descr_words = descr.split()
		line1 = descr_words[0]
		line2 = ""
		for j in range(1, len(descr_words)-1):
			if len(line1 + descr_words[j]) < 28:
				line1 += " " + descr_words[j]
			else:
				if line2 != "":
					line2 += " "
				line2 += descr_words[j]
		line2 += descr_words[-1]
		print(cl(" {0:<38}".format(line1), d_fg, d_bg, 0))
		tline += 1
		fill_or_print_general(tline)
		print(cl(" {0:<38}".format(line2), d_fg, d_bg, 0))
		tline += 1


print()
print(left_indent + cl(hourlydata["hours"], wht, blk, 0))
print("    " + cl("      ", wht, blk, 0) + cl(hourlydata["images"], wht, blu, 0))
print("    " + cl(hourlydata["temp"], wht, blk, 0))
print("    " + cl(hourlydata["rain"], wht, blk, 0))
#print(clouds)


print()
#print(tempsati)