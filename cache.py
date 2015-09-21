#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# cache.py - Cache http calls.
# Author: Chris Barry <chris@barry.im>
# License: Creative Commons Zero

import time
import urllib.error
import urllib.parse
import urllib.request

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
		self.cache[url] = (time.time(), data)
		return data

