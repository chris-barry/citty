#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# weather.py - Holds configuration and code for fetching weather.
# Author: Chris Barry <chris@barry.im>
# License: Creative Commons Zero

import cache
import json
import urllib.parse

class Weather:
	def __init__(self, city='', metric=False, cache_time=60*60):
		self.unit = 'f'
		if metric:
			self.unit = 'c'
		self.cache_time= cache_time
		self.api= 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20\
from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from\
%20geo.places(1)%20where%20text%3D%22{}%22)%20and%20u%3D%22{}%22&\
format=json&env=store%3A%2F%2F\
datatables.org%2Falltableswithkeys'.format(urllib.parse.quote(city), self.unit)
		self.fetcher = cache.CacheFetcher()

	def get(self):
		response = self.fetcher.fetch(self.api, self.cache_time).decode()
		return json.loads(response)

