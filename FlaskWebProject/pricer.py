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
returns lists of prices given the location lists. 
prices will be formatted as tuples: (price, show)
"""
import grequests
import requests
import base64
import json
import datetime
import dateutil
import copy
import tokens

BASE_SABRE_URL = "https://api.test.sabre.com"

def get_sabre_cred():
    client_id = tokens.sabre_clientID
    client_secret = tokens.sabre_clientSecrete
    basic_auth = "Basic " + base64.b64encode(client_id + ":" + client_secret)
    headers = {"Authorization": basic_auth, "Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(BASE_SABRE_URL + "/v1/auth/token", data="grant_type=client_credentials", headers=headers)
    return resp.json()["access_token"]

# ACCESS_TOKEN = get_sabre_cred()

def get_airline_url(FlightNum):
  index = {'UA':'http://united.com', 'AA':'http://aa.com', 'US':'http://usairways.com', 'DL':'http://www.delta.com', 'NK': 'http://www.spirit.com', 'AS':'http://alaskaair.com'}
  if FlightNum[:2] not in index.keys():
    return 'http://google.com'
  else:
    return index[FlightNum[:2]]

def parse_flight_data(json):
    return {
        "Depart": json["FlightSegment"][0]["DepartureDateTime"],
        "Arrive": json["FlightSegment"][-1]["ArrivalDateTime"],
        "FlightNums": map(lambda x: x["OperatingAirline"]["Code"] +x["OperatingAirline"]["FlightNumber"], json["FlightSegment"])
        }

def exception_handler(request, exception):
  print 'Exception'

def air_price(location_list):

    ACCESS_TOKEN = get_sabre_cred()
    baserq = {
      "OTA_AirLowFareSearchRQ": {
        "OriginDestinationInformation": [
          {
            "DepartureDateTime": "2015-04-11T00:00:00",
            "DestinationLocation": {
              "LocationCode": "JFK"
            },
            "OriginLocation": {
              "LocationCode": "LAS"
            },
            "RPH": 1
          },
          {
            "DepartureDateTime": "2015-04-12T00:00:00",
            "DestinationLocation": {
              "LocationCode": "LAS"
            },
            "OriginLocation": {
              "LocationCode": "JFK"
            },
            "RPH": 2
          }
        ],
        "POS": {
          "Source": [
            {
              "RequestorID": {
                "CompanyName": {
                  "Code": "TN"
                },
                "ID": "REQ.ID",
                "Type": "0.AAA.X"
              }
            }
          ]
        },
        "TPA_Extensions": {
          "IntelliSellTransaction": {
            "RequestType": {
              "Name": "50ITINS"
            }
          }
        },
        "TravelPreferences": {
          "TPA_Extensions": {
            "NumTrips": {
              "Number": 1
            }
          }
        },
        "TravelerInfoSummary": {
          "AirTravelerAvail": [
            {
              "PassengerTypeQuantity": [
                {
                  "Code": "ADT",
                  "Quantity": 1
                }
              ]
            }
          ]
        }
      }
      }
    url = BASE_SABRE_URL + "/v1.8.5/shop/flights?mode=live"
    headers = {'content-type': 'application/json',
               'Authorization': "Bearer " + ACCESS_TOKEN
               }
    results = []
    eq_res_store ={}
    async_requests = []
    index = 0
    for x in location_list:
      if x:
        (src, dest, date) = x
        if src == dest:
          eq_res_store[index] = date
        else:
          this_request = copy.deepcopy(baserq)
          this_request["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"][0]["OriginLocation"]["LocationCode"]=src
          this_request["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"][0]["DestinationLocation"]["LocationCode"]=dest
          this_request["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"][0]["DepartureDateTime"]=(date-datetime.timedelta(1)).strftime("%Y-%m-%dT%H:%M:%S")
          this_request["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"][1]["OriginLocation"]["LocationCode"]=dest
          this_request["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"][1]["DestinationLocation"]["LocationCode"]=src
          this_request["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"][1]["DepartureDateTime"]=(date-datetime.timedelta(-1)).strftime("%Y-%m-%dT%H:%M:%S")
          async_requests.append(grequests.post(url, data=json.dumps(this_request), headers=headers))
      else:
        async_requests.append(grequests.post('http://google.com'))
      index += 1
    for r in grequests.map(async_requests):
      try:
        for priced_iternerary in r.json()["OTA_AirLowFareSearchRS"]["PricedItineraries"]["PricedItinerary"]:
            orig_dest_ops = priced_iternerary["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"]

            results.append({
                "There": parse_flight_data(orig_dest_ops[0]),
                "Back": parse_flight_data(orig_dest_ops[1]),
                "TotalPrice": priced_iternerary["AirItineraryPricingInfo"][0]["ItinTotalFare"]["BaseFare"]["Amount"],
                "URL":get_airline_url(parse_flight_data(orig_dest_ops[0])['FlightNums'][0][:2])
                })
      except Exception:
        results.append(None)
    for index in eq_res_store.keys():
      results.insert(index,{'There': {'FlightNums':'No Flight', 'Depart': '', 'Arrive':''}, 'Back': {'FlightNums':'No Flight', 'Depart': '', 'Arrive':''}, 'TotalPrice':0.0, 'URL':'#'})
    return results



        
