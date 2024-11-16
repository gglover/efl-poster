import json
import urllib.parse

leagues_data = None
teams_data = None

with open(f'assets/leagues.json', 'r') as file:
	leagues_data = json.load(file)

with open(f'assets/teams.json', 'r') as file:
	teams_data = json.load(file)

def league_template(data):
	return '\n'.join([f'<div class="team"><img src="badges/{urllib.parse.quote(team)}.png" /></div>' for team in data['teams']])
	
output = f"""
<html>
  <head>
    <title>Football poster</title>
		<link rel="stylesheet" href="base.css" />
	</head>
	<body>
    <main>
      {'\n'.join([league_template(league) for league in leagues_data['leagues']])}
		</main>
		<section>
      <img src="footer.png" />
    </section>
	</body>
</html>
"""

with open("assets/index.html", "w") as index_html:
  index_html.write(output)