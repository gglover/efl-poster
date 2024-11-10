import requests
import json
import time
from bs4 import BeautifulSoup

leagues_data = None

with open('assets/leagues.json', 'r') as file:
	leagues_data = json.load(file)

for index, league in enumerate(leagues_data['leagues']):
	if len(league['teams']) > 0:
		print(f'Skipping {league['name']}: already synced.')
		continue

	time.sleep(2)
	response = requests.get(league['url'])
	soup = BeautifulSoup(response.text, 'html.parser')

	tables = soup.select('table')

	print(f'Parsing team table for {league['name']}')

	team_urls = []

	if len(tables) <= league['table_index']:
		raise ValueError(f'No team table found for {league['name']}')
	
	teams = tables[league['table_index']].select('tbody td:first-child')

	for team in teams:
		team_urls.append(team.find('a').get('href').replace('/wiki/', ''))

	leagues_data['leagues'][index]['teams'] = team_urls

with open('assets/leagues.json', 'w') as file:
	json.dump(leagues_data, file, indent=4)
