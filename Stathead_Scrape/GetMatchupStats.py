import requests
from bs4 import BeautifulSoup

url = "https://stathead.com/baseball/batter_vs_pitcher.cgi?today=1"
print(url)
response = requests.get(url)
content = response.content

soup = BeautifulSoup(content, "html.parser")
print(soup)

# Example: Scraping the player names
player_names = soup.select(".bvp_batter a")
for player_name in player_names:
    print(player_name.text)


