# efl-poster

This repo contains utility scripts to fetch badges and metadata from seven tiers of the English football league system. It also contains a layout script to generate a poster from scraped output.

Download links for full-res posters:

- [2025 - 2026 B1 – Movie Poster Size (27" x 40")](https://gus-city.s3.us-west-2.amazonaws.com/efl-posters/B1-movie-2026.png)
- [2025 - 2026 A1 – Concert Poster Size (24" x 36")](https://gus-city.s3.us-west-2.amazonaws.com/efl-posters/A1-poster-2026.png)

## Scripts

`fetch-leagues.py`

Scrapes wikipedia pages for league pyramid using URLs and selectors from leagues.json config. Makes it easy to regenerate new positions after a promotion / relegation cycle.

`fetch-teams.py`

Scrapes wikipedia pages for team metadata and badge images. Uses team links found from leagues.json.

`generate-poster.py`

Creates HTML file with scraped logos layed out in movie size (27" x 40") poster.

![poster example](assets/example.png)

# More

When I was in high school I made a big poster with five tiers of English Football League clubs. It involved days of manual copying and pasting into photoshop. I decided to revisit the project, double the number of clubs and, automate the process for future years.

You can use Chrome's builtin full-page screenshot command to save a ready-to-print version. `Dev tools > Cmd-P > type ">" > Select Capture full size screenshot`.
