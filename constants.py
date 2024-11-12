# User agent policy for bots: https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy
FETCH_HEADERS = {
	'User-Agent': 'efl-poster-scraper/0.0 (https://github.com/gglover/efl-poster/tree/main; gg@gus.city)'
}

WIKIPEDIA_URL_PREFIX = 'https://en.wikipedia.org/wiki/'

# Respect traffic limits. Sleep a healthy amount between requests.
REQUEST_SLEEP_TIMEOUT_SECONDS = 5