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
		#if self.cache.has_key(url):
		if url in self.cache:
			if int(time.time()) - self.cache[url][0] < max_age:
				return self.cache[url][1]
		# Retrieve and cache
		data = urllib.request.urlopen(url).read()
		self.cache[url] = (time.time(), data)
		return data

def make_panel(h,l, y,x, str):
	win = curses.newwin(h,l, y,x)
	win.erase()
	win.box()
	win.addstr(1, 2, str, curses.A_DIM|curses.A_UNDERLINE)

	panel = curses.panel.new_panel(win)
	return win, panel

def test(stdscr):

	WEATHER_WAIT = 60*60
	WEATHER_URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22union%20city%2C%20nj%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
	try:
		curses.curs_set(0)
	except:
		pass
	stdscr.box()
	stdscr.addstr(2, 2, "Union City Now", curses.A_BOLD)

	time_win, time_panel = make_panel(5,23, 5,5, "Time")
	weather_win, weather_panel = make_panel(8,70, 10,5, "Weather")

	fetcher = CacheFetcher()

	while True:
		foo = fetcher.fetch(WEATHER_URL, WEATHER_WAIT).decode()
		loo = json.loads(foo)
		time_win.addstr(3,2,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

		x = 2
		for day in loo['query']['results']['channel']['item']['forecast']:
			weather_win.addstr(4,x,day['high'])
			weather_win.addstr(5,x,day['low'])

			weather_win.addstr(3,x,day['day'])

			weather_win.addstr(4,x+3,day['text'][:6])

			x = x + 13

		curses.panel.update_panels();
		stdscr.refresh()
		time.sleep(1)


if __name__ == '__main__':
	curses.wrapper(test)
