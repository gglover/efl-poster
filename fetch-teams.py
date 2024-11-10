import requests
import json
import time
from PIL import Image
from bs4 import BeautifulSoup
import sys

# Access the arguments
arguments = sys.argv[1:]  # sys.argv[0] is the script name

# Print the arguments
print("Command-line arguments:", arguments)

WIKIPEDIA_URL_PREFIX = 'https://en.wikipedia.org/wiki/'

leagues_data = None

def fetch_team(name):
	teams_data = None

	with open(f'assets/teams.json', 'r') as file:
		teams_data = json.load(file)

	response = requests.get(f'{WIKIPEDIA_URL_PREFIX}{name}')
	soup = BeautifulSoup(response.text, 'html.parser')

	print(f'Parsing team data for {name}')

	infobox = soup.select('table.infobox.vcard')
	if infobox is None or len(infobox) == 0:
		raise ValueError(f'No info found for {name}')
	
	infobox = infobox[0]

	badge_url = infobox.select('img')[0].get('src')
	badge_url = f'https:{badge_url}'

	with Image.open(requests.get(badge_url, stream=True).raw) as badge_img:
		badge_img.save(f'assets/badges/{name}.png', 'PNG')

	print(badge_url)

	# fields = []
	# for i, row in enumerate(infobox.find_all('tr')):
	# 	fields.append(row.find('th').text.strip())
	# 	fields.append(row.find('td').text.strip())
	
	# print(headers)
	# print(rows)

	# with open('assets/teams.json', 'w') as file:
	# 	json.dump(teams_data, file, indent=4)

fetch_team('Arsenal_F.C.')