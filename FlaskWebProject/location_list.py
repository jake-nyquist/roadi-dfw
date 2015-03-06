    # Roadi
    # Copyright (C) 2014 Jake Nyquist, Philip Taffet, Brett Gutstein

    # This program is free software; you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation; either version 2 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License along
    # with this program; if not, write to the Free Software Foundation, Inc.,
    # 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
    
    # To contact the authors, write us at nyquist11 (at) gmail (dot) com

"""
Makes a list of locations and times from the search
"""
import requests
import tokens

stubhub_token = tokens.stubhub_token
base_uri = 'https://api.stubhub.com/'

def get_location(ipaddress):
    if type(ipaddress) != str:
        print 'IP is not a string'
        return 0
    r = requests.get('http://www.telize.com/geoip/'+ipaddress)
    return r.json()['city']

#print get_location('128.42.66.21')

def get_stubhub(query, startingDate, endingDate, page):
    headers = {'content-type': 'application/json',
               'Authorization': "Bearer " + stubhub_token
               }
    uri = base_uri + 'search/catalog/events/v2'
    httpquery = {'title': query +' -\"PARKING PASSES ONLY\"'
                 , 'sort':'minPrice asc', 'limit': 40, 'start': 20*page, 'minAvailableTickets':1, 'date':startingDate +' TO ' + endingDate}
    resp = requests.get(uri, headers = headers, params= httpquery)
    if resp.status_code != 200:
        print 'An Error has occured from Stubhub. (Error: %i): %s' % (resp.status_code, resp.text)
        return False
    responses = resp.json()
    if responses['numFound'] == 0:
        print 'No Responses were found for your query!'
        return False
    event_list = []
    for event in responses['events']:
        event_dict = {}
        if event['status'] == 'Cancelled' or event['status'] == 'Completed':
            print "Skipping event with status ", event['status']
            continue
        if len(event['title']) > 20 and event['title'][:19] == 'PARKING PASSES ONLY':
            print "Skipping event with title ", event['title']
            continue
        event_dict['price'] = event['ticketInfo']['minPrice']
        event_dict['title'] = event['title']
        event_dict['url'] = event['eventInfoUrl']
        event_dict['date'] = event['dateUTC']
        event_dict['location'] = event['venue']['city']
        event_list.append(event_dict)
    return event_list
#print get_stubhub('Houston Rockets', None, None)





