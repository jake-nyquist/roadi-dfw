"""
Module that processes the query into a results page. 

"""
# Roadi, finding the lowest cost to see your favorite app. 
#     Copyright (C) 2015 Philip Taffet, Jake Nyquist, Brett Gutstein

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import location_list
import pricer
from dateutil.parser import parse
import datetime
from airports import airports

def flight_link_gen(flightStr):
	return NotImplementedError

def get_date_string(string):
	return parse(string).strftime("%a, %b %d %Y")

def get_time_string(string):
	return parse(string).strftime("%I:%M %p")

def get_flight_string(list_of_flights):
	if type(list_of_flights) == list:
		return ", ".join(list_of_flights)
	else:
		return list_of_flights

def process_query(query, startingDate, endingDate, startCity, page):
	print query, startingDate, endingDate, startCity
	events = location_list.get_stubhub(query, startingDate, endingDate, page)
	print events
	if events == False:
		return {'success': False, 'items': []}
	loc_list = []
	for event in events:
		if airports(event['location']) == None:
			#print 'remove because of apt:',event['location']
			loc_list.append(None)
			continue
		loc_list.append((startCity,airports(event['location']), parse(event['date'])))
	air_results = pricer.air_price(loc_list)
	events_list = []
	for index in range(len(events)):
		if air_results[index] == None:
			pass
			#print'remove because of air result:',loc_list[index]
		else:
			event_dic = {}
			event_dic['title'] = events[index]['title']
			event_dic['date'] = get_date_string(events[index]['date'])
			event_dic['city'] = events[index]['location']
			event_dic['travelPrice'] = '$%.2f' %air_results[index]['TotalPrice']
			event_dic['price'] = '$%.2f' %float(events[index]['price']+air_results[index]['TotalPrice'])
			event_dic['admission'] = {'price': '$%.2f' %float(events[index]['price']), 'link': events[index]['url']}
			if air_results[index]['URL'] =='#':
				air_results[index]['URL'] = 'https://www.google.com/maps/place/'+events[index]['location']
			#print air_results[index]
			event_dic['outbound'] = {'link' : air_results[index]['URL'], 
										'name':get_flight_string(air_results[index]['There']['FlightNums']),
										'homePort':startCity, 'destPort':airports(events[index]['location']), 'date':get_date_string(air_results[index]['There']['Depart']), 'start': get_time_string(air_results[index]['There']['Depart']),'end':get_time_string(air_results[index]['There']['Arrive'])}
			event_dic['inbound'] = {'link' : air_results[index]['URL'], 
										'name': get_flight_string(air_results[index]['Back']['FlightNums']),
										'destPort':startCity, 'homePort':airports(events[index]['location']), 'date':get_date_string(air_results[index]['Back']['Depart']), 'start': get_time_string(air_results[index]['Back']['Depart']),'end':get_time_string(air_results[index]['Back']['Arrive'])}
			events_list.append(event_dic)
	events_list.sort(key=lambda x:float(x['price'][1:]))
	if events_list == []:
		return {'success':False, 'events':[]}
	return {'success':True, 'events': events_list}


#print pricer.air_price([('IAH', u'DCA', datetime.datetime(2015, 8, 6, 0, 5))])
#print process_query('Fleetwood Mac', '2015-03-01T20:30', '2015-12-17T20:30', 'DFW')
#print process_query('Houston Astros', '2015-03-01T20:30', '2015-12-17T20:30', 'IAH')
#print parse('2015-04-17T20:30:00-6:00').strftime("%Y-%M-%dT%H:%M")
#print pricer.air_price([(u'IAH', 'LGA', parse('2015-04-17T20:30:00-6:00'))])









