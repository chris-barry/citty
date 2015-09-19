#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# panel.py - Home screen for my apartment.
# Author: Chris Barry <chris@barry.im>
# License:  Creative Commons Zero

import time
import urllib.request, urllib.parse, urllib.error
import curses
import curses.panel
import json

class CacheFetcher:
	def __init__(self):
		self.cache = {}

	def fetch(self, url, max_age=0):
		if url in self.cache:
			if int(time.time()) - self.cache[url][0] < max_age:
				return self.cache[url][1]

		# Retrieve and cache
		try:
			data = urllib.request.urlopen(url).read()
		except IOError:
			# Return last cache if we have it
			if url in self.cache:
				return self.cache[url][1]
			else:
				data = None

		# PUT TRY AROUND THIS
		self.cache[url] = (time.time(), data)
		return data

# Holds configuration and code for fetching weather
class Weather:
	def __init__(self, city='', metric=False, cache_time=60*60):
		self.unit = 'f'
		if metric:
			self.unit = 'c'
		self.CACHE_TIME = cache_time
		self.API = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22{}%22)%20and%20u%3D%22{}%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'.format(urllib.parse.quote(city), self.unit)
		self.fetcher = CacheFetcher()

	def get(self):
		response = self.fetcher.fetch(self.API, self.CACHE_TIME).decode()
		return json.loads(response)

def make_panel(h,l, y,x, str):
	win = curses.newwin(h,l, y,x)
	win.erase()
	win.box()
	win.addstr(1, 2, str, curses.A_UNDERLINE)

	panel = curses.panel.new_panel(win)
	return win, panel

def test(stdscr):

	# Seconds
	REFRESH_DELAY = 10
	#REFRESH_DELAY = 60
	TITLE = "Things Today"
	WEATHER_TITLE = "Weather"
	TRANSIT_TITLE = "Transit"

	WEATHER_CITY = "Union City, NJ"

	try:
		curses.curs_set(0)
	except:
		pass
	stdscr.box()
	stdscr.addstr(1, 1, TITLE, curses.A_BOLD)

	# Panels
	weather_win, weather_panel = make_panel(8,75, 3,2, WEATHER_TITLE)

	# APIs and stuff
	weather = Weather(city=WEATHER_CITY, metric=False)

	while True:
		# ----- BEGIN TIME -----
		stdscr.addstr(1, len(TITLE)+1,time.strftime(" - %Y-%m-%d %H:%M",))
		# ----- END TIME -----

		# ----- BEGIN WEATHER -----
		w = weather.get()
		u = weather.unit.upper()

		x = 2
		width = 16
		for day in w['query']['results']['channel']['item']['forecast']:
			weather_win.addstr(3,x,day['day'])
			weather_win.addstr(4,x,'{}{}'.format(day['high'],u))
			weather_win.addstr(5,x,'{}{}'.format(day['low'],u))
			weather_win.addstr(6,x,day['text'][:width-1])
			x = x + width
		weather_win.addstr(1,len(WEATHER_TITLE)+3,'- '+w['query']['results']['channel']['title'], curses.A_DIM)
		# ----- END WEATHER -----

		# ----- BEGIN TRANSIT -----
		# ----- END TRANSIT -----

		curses.panel.update_panels();
		stdscr.refresh()
		time.sleep(REFRESH_DELAY)


if __name__ == '__main__':
	curses.wrapper(test)
