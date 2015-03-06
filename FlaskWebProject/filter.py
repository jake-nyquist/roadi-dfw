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
import json

f = open("airports.json")

j = json.load(f)

mapping = {}
choices = []
for airp in j:
	if airp['country'] == 'United States' and int(airp['direct_flights']) >= 30:
		mapping[airp['city']] = airp['code']
		choices.append(airp['city'])

		mapping[airp['city'] + " (" + airp['name'] + ")"] = airp['code']
		choices.append(airp['city'] + " (" + airp['name'] + ")")

		mapping[airp['code']] = airp['code']
		choices.append(airp['code'])

f.close()
f = open("MAC.json")
j = json.load(f)

for mac in j['Cities']:
	mapping[mac['name']] = mac['code']
	choices.append(mac['name'])

print "from fuzzywuzzy import fuzz"
print "from fuzzywuzzy import process"
print
print "mapping = " + str(mapping)
print "choices = " + str(choices)

print """
def airports(string):
	res = process.extractOne(string, choices, scorer=fuzz.token_set_ratio)
	if res[1] >= 80:
		return mapping[res[0]]
	else:
		return None
"""
