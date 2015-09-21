#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# transit.py - Get times for transit.
# Author: Chris Barry <chris@barry.im>
# License: Creative Commons Zero

import csv
import datetime
import io
import pprint
import os.path
import zipfile

# NOTES:
# Direction 0 means into NYC for my use case.
# Undocumented service IDs:
#   1  = sat
#   2  = sun
#   3  = weekday
#   4+ = undetermined

# Fuck new jersey transit.
class NJTransit:
	def __init__(self, gtfs='', stop_id='', route_id='', direction=0):
		self.gtfs = gtfs
		self.stop_id = stop_id
		self.route_id = route_id 
		self.direction = direction

		if not os.path.isfile(self.gtfs):
			raise IOError('GTFS file not found.')

		if not zipfile.is_zipfile(self.gtfs):
			raise zipfile.BadZipFile('Bad file.')

		zip_internal = zipfile.ZipFile(self.gtfs, 'r')

		weekday_trips = []
		sat_trips = []
		sun_trips = []

		with io.TextIOWrapper(zip_internal.open('trips.txt')) as t:
			trips_reader = csv.DictReader(t)
			# TODO: This doesn't take in to account holidays.
			for row in trips_reader:
				if int(row['route_id']) == route_id and int(row['direction_id']) == 0 and int(row['service_id']) == 3:
					weekday_trips.append(row['trip_id'])
				if int(row['route_id']) == route_id and int(row['direction_id']) == 0 and int(row['service_id']) == 1:
					sat_trips.append(row['trip_id'])
				if int(row['route_id']) == route_id and int(row['direction_id']) == 0 and int(row['service_id']) == 2:
					sun_trips.append(row['trip_id'])

		weekday_trip_times = []
		sat_trip_times = []
		sun_trip_times = []

		zip_internal = zipfile.ZipFile(self.gtfs, 'r')
		with io.TextIOWrapper(zip_internal.open('stop_times.txt')) as f:
			times_reader = csv.DictReader(f)
			for row in times_reader:
				if row['trip_id'] in weekday_trips and int(row['stop_id']) == self.stop_id:
					weekday_trip_times.append(row['departure_time'])
				if row['trip_id'] in sat_trips and int(row['stop_id']) == self.stop_id:
					sat_trip_times.append(row['departure_time'])
				if row['trip_id'] in sun_trips and int(row['stop_id']) == self.stop_id:
					sun_trip_times.append(row['departure_time'])

		self.weekday_trip_times = sorted(weekday_trip_times)
		self.sat_trip_times = sorted(sat_trip_times)
		self.sun_trip_times = sorted(sun_trip_times)

	# Parse the trips based on the day of week.
	def get_times(self, limit=5):
		now = datetime.datetime.now()
		if now.strftime('%a') == 'Sat':
			times = self.sat_trip_times
			times_tom = self.sun_trip_times
		elif now.strftime('%a') == 'Sun':
			times = self.sun_trip_times
			times_tom = self.weekday_trip_times
		elif now.strftime('%a') == 'Fri':
			times = self.weekday_trip_times
			times_tom = self.sat_trip_times
		else:
			times = self.weekday_trip_times
			times_tom = self.weekday_trip_times

		n = now.strftime('%H:%M')
		i = 0
		for t in times:
			if n < t:
				break
			i = i + 1
				
		today = times[i:i+limit]
		overflow = times_tom[0:limit-len(today)]
		return today + overflow

