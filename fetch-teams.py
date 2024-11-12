import requests
import json
import time
import io
import re
import os.path
from PIL import Image
from bs4 import BeautifulSoup
from constants import FETCH_HEADERS, WIKIPEDIA_URL_PREFIX, REQUEST_SLEEP_TIMEOUT_SECONDS

def fetch_team(name):
	# Fetch html from wikipedia for team.
	teams_data = None
	with open(f'assets/teams.json', 'r') as file:
		teams_data = json.load(file)

	if (name in teams_data):
		print(f'{name}: Already synced')
		return

	response = requests.get(f'{WIKIPEDIA_URL_PREFIX}{name}', headers=FETCH_HEADERS)
	time.sleep(REQUEST_SLEEP_TIMEOUT_SECONDS)

	# Extract text info from "infobox". Consistent across team pages.
	wiki_data = BeautifulSoup(response.text, 'html.parser')
	print(f'{name}: Parsing team data')

	infobox = wiki_data.select_one('table.infobox.vcard')
	if infobox is None:
		raise ValueError(f'{name}: No info found')
	
	team_data = {
		"name": wiki_data.select_one('h1').text.strip(),
		"nickname": None,
		"founded": None,
		"ground": None
	}

	for i, row in enumerate(infobox.find_all('tr')):
		header = row.find('th')
		value = row.find('td')
		
		if header != None and value != None:
			header = header.text.strip()
			value = value.text.strip()

			if re.match("ground", header, re.IGNORECASE):
				team_data["ground"] = value

			if re.match("nickname", header, re.IGNORECASE):
				team_data["nickname"] = value
			
			if re.match("founded", header, re.IGNORECASE):
				# Try to extract a single 4 digit year from the date.
				year_match = re.search(r'\b\d{4}\b', value)

				if year_match:
					first_year = year_match.group()
					team_data["founded"] = first_year
	
	# Write parsed data teams.json
	teams_data[name] = team_data

	with open('assets/teams.json', 'w') as file:
		json.dump(teams_data, file, indent=4)

	# Extract badge URL from "infobox"
	badge_url = infobox.select_one('img').get('src')
	badge_url = f'https:{badge_url}'
	badge_output_path = f'assets/badges/{name}.png'

	if (os.path.isfile(badge_output_path)):
		print(f'{name}: Badge already exists')
		return
	
	# Fetch badge and convert to PNG with consistent naming.
	print(f'{name}: Fetching badge - {badge_url}')
	time.sleep(REQUEST_SLEEP_TIMEOUT_SECONDS)

	badge_img_data = requests.get(badge_url, stream=True, headers=FETCH_HEADERS)
	
	if badge_img_data.status_code != 200:
		print(f'Failed to fetch badge. Status code {badge_img_data.status_code}')
		return

	with Image.open(io.BytesIO(badge_img_data.content)) as badge_img:
		badge_img.save(badge_output_path, 'PNG')

with open('assets/leagues.json', 'r') as file:
	leagues_data = json.load(file)

	for league in leagues_data['leagues']:
		for team in league['teams']:
			fetch_team(team)