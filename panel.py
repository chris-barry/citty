#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# panel.py - Home screen for my apartment.
# Author: Chris Barry <chris@barry.im>
# License:  Creative Commons Zero

import curses
import curses.panel
import time
import weather

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
	weather_a = weather.Weather(city=WEATHER_CITY, metric=False)

	while True:
		# ----- BEGIN TIME -----
		stdscr.addstr(1, len(TITLE)+1,time.strftime(" - %Y-%m-%d %H:%M",))
		# ----- END TIME -----

		# ----- BEGIN WEATHER -----
		w = weather_a.get()
		u = weather_a.unit.upper()

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

