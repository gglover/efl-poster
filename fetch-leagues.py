import requests
import json
import time
from bs4 import BeautifulSoup
from constants import FETCH_HEADERS, REQUEST_SLEEP_TIMEOUT_SECONDS

# This script parses league overview pages and syncronizes the teams
# in a league for a given season. Should only need to run this once after
# each promotion / relegation cycle.

leagues_data = None

with open('assets/leagues.json', 'r') as file:
	leagues_data = json.load(file)
	
for index, league in enumerate(leagues_data['leagues']):
	if len(league['teams']) > 0:
		print(f'Skipping {league['name']}: already synced – {len(league['teams'])} teams total')
		continue

	# Fetch current seaeson's overview wikipedia page for the league
	response = requests.get(league['url'], headers=FETCH_HEADERS)
	time.sleep(REQUEST_SLEEP_TIMEOUT_SECONDS)

	soup = BeautifulSoup(response.text, 'html.parser')

	tables = soup.select('table')
	print(f'Parsing team table for {league['name']}')

	team_urls = []

	if len(tables) <= league['table_index']:
		raise ValueError(f'No team table found for {league['name']}')
	
	# Select manually identified table index containing alphapetical links to teams.
	# Iterate teamss and append to metadata.
	teams = tables[league['table_index']].select('tbody td:first-child')

	for team in teams:
		team_urls.append(team.find('a').get('href').replace('/wiki/', ''))

	leagues_data['leagues'][index]['teams'] = team_urls

# Update leagues.json with new data.
with open('assets/leagues.json', 'w') as file:
	json.dump(leagues_data, file, indent=4)
