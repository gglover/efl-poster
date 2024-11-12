import json
import urllib.parse

leagues_data = None
with open(f'assets/leagues.json', 'r') as file:
	leagues_data = json.load(file)

def league_template(data):
	teams_content = [f'<div class="team"><img src="badges/{urllib.parse.quote(team)}.png" /></div>' for team in data['teams']]
	
	return f"""
	{'\n'.join(teams_content)} 
	"""
	
output = f"""
<html>
  <head>
    <title>Football poster</title>
		<link rel="stylesheet" href="poster/base.css" />
	</head>
	<body>
    <main>
      {'\n'.join([league_template(league) for league in leagues_data['leagues']])}
		</main>
	</body>
</html>
"""

with open("assets/index.html", "w") as index_html:
  index_html.write(output)