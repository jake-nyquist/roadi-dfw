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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

mapping = {u'JFK': u'JFK', u'Dania Beach': u'FLL', u'MIA': u'MIA', u'Arlington': u'DCA', u'BOS': u'BOS', u'OAK': u'OAK', u'Fairbanks (Fairbanks International Airport)': u'FAI', u'Newark': u'EWR', u'SJC': u'SJC', u'Carolina (Luis Munoz Marin Airport)': u'SJU', u'San Francisco': u'SFO', u'Tampa - St Petersburg': u'TPA', u'Anchorage (Anchorage International Airport)': u'ANC', u'SAN': u'SAN', u'St. Paul (Minneapolis St Paul International Airport)': u'MSP', u'Sacramento': u'SMF', u'Louisville (Louisville International Airport)': u'SDF', u'Las Vegas (Mccarran International Airport)': u'LAS', u'DCA': u'DCA', u'Cleveland (Hopkins International Airport)': u'CLE', u'Swanton (Toledo Express Airport)': u'TOL', u'Indianapolis (Indianapolis International Airport)': u'IND', u'BWI': u'BWI', u'Atlanta': u'ATL', u'Seattle (Tacoma International Airport)': u'SEA', u'PIT': u'PIT', u'Fairbanks': u'FAI', u'Tampa': u'TPA', u'Los Angeles': u'LAX', u'Fort Myers (Southwest Florida International Airport)': u'RSW', u'Bullhead City': u'IFP', u'Windsor Locks (Bradley International Airport)': u'BDL', u'IAH': u'IAH', u'JAX': u'JAX', u'Charlotte': u'CLT', u'Miami': u'MIA', u'IAD': u'IAD', u'West Palm Beach (Palm Beach International Airport)': u'PBI', u'San Jose (Norman Y Mineta San Jose International Airport)': u'SJC', u'Birmingham (Birmingham International Airport)': u'BHM', u'Salt Lake City (Salt Lake City International Airport)': u'SLC', u'Arlington (Washington National Airport)': u'DCA', u'BNA': u'BNA', u'Sacramento (Sacramento International Airport)': u'SMF', u'Coraopolis (Pittsburgh International Airport)': u'PIT', u'Jacksonville (Jacksonville International Airport)': u'JAX', u'Charlotte (Douglas International Airport)': u'CLT', u'Jamaica': u'JFK', u'Cincinnati': u'CVG', u'PHL': u'PHL', u'Honolulu (Honolulu International Airport)': u'HNL', u'Washington': u'WAS', u'Jacksonville': u'JAX', u'SFO': u'SFO', u'PHX': u'PHX', u'LAX': u'LAX', u'Wilmington (Airborne Airpark)': u'ILN', u'SAT': u'SAT', u'Seattle': u'SEA', u'Austin (Austin-Bergstrom International Airport)': u'AUS', u'LAS': u'LAS', u'IFP': u'IFP', u'CMH': u'CMH', u'Chicago (Chicago Midway International Airport)': u'MDW', u'Denver': u'DEN', u'Newark (Newark International Airport)': u'EWR', u'Raleigh/Durham (Durham International Airport)': u'RDU', u'FLL': u'FLL', u'DEN': u'DEN', u'Kansas City (Kansas City International Airport)': u'MCI', u'Windsor Locks': u'BDL', u'DTW': u'DTW', u'Nashville (Nashville International Airport)': u'BNA', u'Bullhead City (Laughlin-Bullhead International Airport)': u'IFP', u'Houston (William P Hobby Airport)': u'HOU', u'San Diego': u'SAN', u'Albuquerque': u'ABQ', u'Albuquerque (Albuquerque International Airport)': u'ABQ', u'Honolulu': u'HNL', u'Salt Lake City': u'SLC', u'San Antonio': u'SAT', u'Kenner': u'MSY', u'Killeen': u'ILE', u'BDL': u'BDL', u'San Jose': u'SJC', u'Memphis (Memphis International Airport)': u'MEM', u'EWR': u'EWR', u'Panama City': u'PFN', u'PBI': u'PBI', u'ORD': u'ORD', u'Atlanta (Hartsfield-Jackson Atlanta International Airport)': u'ATL', u'St. Louis (Lambert St Louis International Airport)': u'STL', u'Clinton': u'CSM', u'ANC': u'ANC', u'Boston': u'BOS', u'Altus': u'LTS', u'Oakland (Oakland International Airport)': u'OAK', u'Las Vegas': u'LAS', u'Dania Beach (Fort Lauderdale Hollywood International Airport)': u'FLL', u'IND': u'IND', u'Jamaica (John F Kennedy International Airport)': u'JFK', u'Baltimore (Baltimore-Washington International Thurgood Mars)': u'BWI', u'Dallas': u'DFW', u'ILN': u'ILN', u'ATL': u'ATL', u'HNL': u'HNL', u'Los Angeles (Los Angeles International Airport)': u'LAX', u'Louisville': u'SDF', u'Detroit (Detroit Metropolitan Wayne County Airport)': u'DTW', u'Flushing': u'LGA', u'SMF': u'SMF', u'Columbus': u'CMH', u'Indianapolis': u'IND', u'Sault Ste Marie': u'SSM', u'Phoenix (Sky Harbor International Airport)': u'PHX', u'Kenner (New Orleans International Airport)': u'MSY', u'Hebron (Greater Cincinnati International Airport)': u'CVG', u'Flushing (LaGuardia Airport)': u'LGA', u'SEA': u'SEA', u'Memphis': u'MEM', u'MDW': u'MDW', u'RDU': u'RDU', u'St. Louis': u'STL', u'PDX': u'PDX', u'CLE': u'CLE', u'DFW': u'DFW', u'Orlando': u'ORL', u'Detroit': u'DTT', u'West Palm Beach': u'PBI', u'Dallas - Fort Worth': u'QDF', u'AUS': u'AUS', u'CLT': u'CLT', u'San Diego (San Diego International Airport)': u'SAN', u'Fayetteville': u'FYV', u'MSP': u'MSP', u'Austin': u'AUS', u'Raleigh/Durham': u'RDU', u'Portland (Portland International Airport)': u'PDX', u'Tampa (Tampa International Airport)': u'TPA', u'MEM': u'MEM', u'Hebron': u'CVG', u'Columbus (Port Columbus International Airport)': u'CMH', u'New York': u'NYC', u'Birmingham': u'BHM', u'Cleveland': u'CLE', u'Houston (George Bush Intercontinental Airport)': u'IAH', u'Coraopolis': u'PIT', u'Milwaukee (General Mitchell International Airport)': u'MKE', u'San Antonio (San Antonio International Airport)': u'SAT', u'MKE': u'MKE', u'Miami (Miami International Airport)': u'MIA', u'MSY': u'MSY', u'Chicago': u'CHI', u'Atlantic City': u'AIY', u'Dallas (Fort Worth International Airport)': u'DFW', u'Denver (Denver International Airport)': u'DEN', u'Philadelphia (Philadelphia International Airport)': u'PHL', u'TOL': u'TOL', u'CVG': u'CVG', u'Fort Myers': u'FMY', u'Springfield': u'SFY', u'TPA': u'TPA', u'Phoenix': u'PHX', u'San Francisco (San Francisco International Airport)': u'SFO', u'Nashville': u'BNA', u'Harrisburg': u'HAR', u'FAI': u'FAI', u'Hartford': u'HFD', u'Carolina': u'SJU', u'Boston (Gen E L Logan International Airport)': u'BOS', u'Swanton': u'TOL', u'STL': u'STL', u'Anchorage': u'ANC', u'Wilmington': u'ILN', u'Kansas City': u'MKC', u'ABQ': u'ABQ', u'HOU': u'HOU', u'Washington (Dulles International Airport)': u'IAD', u'Orlando (Orlando International Airport)': u'MCO', u'SJU': u'SJU', u'Baltimore': u'BWI', u'SLC': u'SLC', u'MCO': u'MCO', u'Houston': u'QHO', u'RSW': u'RSW', u'BHM': u'BHM', u'MCI': u'MCI', u'Philadelphia': u'QPH', u'LGA': u'LGA', u'Steamboat Springs': u'SBS', u"Chicago (Chicago O'Hare International Airport)": u'ORD', u'SDF': u'SDF', u'Milwaukee': u'MKE', u'Portland': u'PDX', u'Oakland': u'OAK', u'St. Paul': u'MSP'}
choices = [u'Albuquerque', u'Albuquerque (Albuquerque International Airport)', u'ABQ', u'Anchorage', u'Anchorage (Anchorage International Airport)', u'ANC', u'Atlanta', u'Atlanta (Hartsfield-Jackson Atlanta International Airport)', u'ATL', u'Austin', u'Austin (Austin-Bergstrom International Airport)', u'AUS', u'Windsor Locks', u'Windsor Locks (Bradley International Airport)', u'BDL', u'Birmingham', u'Birmingham (Birmingham International Airport)', u'BHM', u'Nashville', u'Nashville (Nashville International Airport)', u'BNA', u'Boston', u'Boston (Gen E L Logan International Airport)', u'BOS', u'Baltimore', u'Baltimore (Baltimore-Washington International Thurgood Mars)', u'BWI', u'Cleveland', u'Cleveland (Hopkins International Airport)', u'CLE', u'Charlotte', u'Charlotte (Douglas International Airport)', u'CLT', u'Columbus', u'Columbus (Port Columbus International Airport)', u'CMH', u'Hebron', u'Hebron (Greater Cincinnati International Airport)', u'CVG', u'Arlington', u'Arlington (Washington National Airport)', u'DCA', u'Denver', u'Denver (Denver International Airport)', u'DEN', u'Dallas', u'Dallas (Fort Worth International Airport)', u'DFW', u'Detroit', u'Detroit (Detroit Metropolitan Wayne County Airport)', u'DTW', u'Newark', u'Newark (Newark International Airport)', u'EWR', u'Fairbanks', u'Fairbanks (Fairbanks International Airport)', u'FAI', u'Dania Beach', u'Dania Beach (Fort Lauderdale Hollywood International Airport)', u'FLL', u'Honolulu', u'Honolulu (Honolulu International Airport)', u'HNL', u'Houston', u'Houston (William P Hobby Airport)', u'HOU', u'Washington', u'Washington (Dulles International Airport)', u'IAD', u'Houston', u'Houston (George Bush Intercontinental Airport)', u'IAH', u'Bullhead City', u'Bullhead City (Laughlin-Bullhead International Airport)', u'IFP', u'Wilmington', u'Wilmington (Airborne Airpark)', u'ILN', u'Indianapolis', u'Indianapolis (Indianapolis International Airport)', u'IND', u'Jacksonville', u'Jacksonville (Jacksonville International Airport)', u'JAX', u'Jamaica', u'Jamaica (John F Kennedy International Airport)', u'JFK', u'Las Vegas', u'Las Vegas (Mccarran International Airport)', u'LAS', u'Los Angeles', u'Los Angeles (Los Angeles International Airport)', u'LAX', u'Flushing', u'Flushing (LaGuardia Airport)', u'LGA', u'Kansas City', u'Kansas City (Kansas City International Airport)', u'MCI', u'Orlando', u'Orlando (Orlando International Airport)', u'MCO', u'Chicago', u'Chicago (Chicago Midway International Airport)', u'MDW', u'Memphis', u'Memphis (Memphis International Airport)', u'MEM', u'Miami', u'Miami (Miami International Airport)', u'MIA', u'Milwaukee', u'Milwaukee (General Mitchell International Airport)', u'MKE', u'St. Paul', u'St. Paul (Minneapolis St Paul International Airport)', u'MSP', u'Kenner', u'Kenner (New Orleans International Airport)', u'MSY', u'Oakland', u'Oakland (Oakland International Airport)', u'OAK', u'Chicago', u"Chicago (Chicago O'Hare International Airport)", u'ORD', u'West Palm Beach', u'West Palm Beach (Palm Beach International Airport)', u'PBI', u'Portland', u'Portland (Portland International Airport)', u'PDX', u'Philadelphia', u'Philadelphia (Philadelphia International Airport)', u'PHL', u'Phoenix', u'Phoenix (Sky Harbor International Airport)', u'PHX', u'Coraopolis', u'Coraopolis (Pittsburgh International Airport)', u'PIT', u'Raleigh/Durham', u'Raleigh/Durham (Durham International Airport)', u'RDU', u'Fort Myers', u'Fort Myers (Southwest Florida International Airport)', u'RSW', u'San Diego', u'San Diego (San Diego International Airport)', u'SAN', u'San Antonio', u'San Antonio (San Antonio International Airport)', u'SAT', u'Louisville', u'Louisville (Louisville International Airport)', u'SDF', u'Seattle', u'Seattle (Tacoma International Airport)', u'SEA', u'San Francisco', u'San Francisco (San Francisco International Airport)', u'SFO', u'San Jose', u'San Jose (Norman Y Mineta San Jose International Airport)', u'SJC', u'Carolina', u'Carolina (Luis Munoz Marin Airport)', u'SJU', u'Salt Lake City', u'Salt Lake City (Salt Lake City International Airport)', u'SLC', u'Sacramento', u'Sacramento (Sacramento International Airport)', u'SMF', u'St. Louis', u'St. Louis (Lambert St Louis International Airport)', u'STL', u'Swanton', u'Swanton (Toledo Express Airport)', u'TOL', u'Tampa', u'Tampa (Tampa International Airport)', u'TPA', u'Altus', u'Atlantic City', u'Chicago', u'Cincinnati', u'Clinton', u'Dallas - Fort Worth', u'Detroit', u'Fayetteville', u'Fort Myers', u'Harrisburg', u'Hartford', u'Houston', u'Kansas City', u'Killeen', u'New York', u'Orlando', u'Panama City', u'Philadelphia', u'Sault Ste Marie', u'Seattle', u'Springfield', u'Steamboat Springs', u'Tampa - St Petersburg', u'Washington']

def airports(string):
	res = process.extractOne(string, choices, scorer=fuzz.token_set_ratio)
	if res[1] >= 80:
		return mapping[res[0]]
	else:
		print "Failed to convert" , string, "to an airport"
		return None

