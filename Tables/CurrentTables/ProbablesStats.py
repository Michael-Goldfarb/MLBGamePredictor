import requests
import json
import psycopg2
from datetime import datetime
import os

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_port = os.environ.get('DB_PORT')
db_password = os.environ.get('DB_PASSWORD')

# Use the variables in your psycopg2.connect() call:
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    port=db_port,
    password=db_password
)

cursor = conn.cursor()
unique_games = []
game_ids = set()
starters = []
gameIdss = []
teamsStarters = []
startersName = []
teamIds = []
response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
# response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-07-22&endDate=2023-07-22")
data = response.json()
games = data['dates'][0]['games']

# Loop through each gameId
for game in games:
    gameId = game['gamePk']
    gameIdss.append(gameId)
    gameIdss.append(gameId)
    if gameId not in game_ids:
        unique_games.append(game)
        game_ids.add(gameId)
for game in unique_games:
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game['gamePk']}/feed/live"
    response = requests.get(url)
    data = response.json()

    awayTeamName = data['gameData']['teams']['away']['name']
    homeTeamName = data['gameData']['teams']['home']['name']
    awayTeamId = data['gameData']['teams']['away']['id']
    homeTeamId = data['gameData']['teams']['home']['id']
    probablePitcherHome = data['gameData']['probablePitchers'].get('home')
    probablePitcherHomeId = probablePitcherHome.get('id') if probablePitcherHome else None
    starters.append(probablePitcherHomeId)
    startersName.append(probablePitcherHome['fullName'] if probablePitcherHome else None)
    teamsStarters.append(homeTeamName)
    teamIds.append(homeTeamId)
    probablePitcherAway = data['gameData']['probablePitchers'].get('away')
    probablePitcherAwayId = probablePitcherAway.get('id') if probablePitcherAway else None
    starters.append(probablePitcherAwayId)
    startersName.append(probablePitcherAway['fullName'] if probablePitcherAway else None)
    teamsStarters.append(awayTeamName)
    teamIds.append(awayTeamId)

# Define the SQL statement to create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS probablesStats (
        player_id TEXT,
        gameId TEXT,
        teamId VARCHAR(255),
        player_name TEXT,
        strikeoutWalkRatio TEXT,
        games_started INTEGER,
        hitsPer9Inn TEXT,
        strikeoutsPer9Inn TEXT,
        team_name TEXT,
        era TEXT,
        whip TEXT,
        walksPer9Inn TEXT
    );
""")

# Truncate the table before inserting new data
cursor.execute("TRUNCATE TABLE probablesStats;")

for index, player_id in enumerate(starters):
    team_name = teamsStarters[index]  # Get the team name corresponding to the current player
    player_name = startersName[index]
    teamId = teamIds[index]
    print(player_name)
    gamesId = gameIdss[index]
    print(gamesId)

    # Make the API request to fetch player stats
    api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2024&group=pitching&startDate=03/28/2024&endDate={currentDate}&leagueListId=mlb_milb".format(
        playerId=player_id,
        # currentDate=datetime.now().strftime("%m/%d/%Y")  
        currentDate = "09-25-2023"
    )
    response = requests.get(api_url)
    data = response.json()
    if 'stats' in data:
        for stat in data['stats']:
            for split in stat["splits"]:
                if split["sport"]["abbreviation"] == "MLB":
                    era = split["stat"]["era"]
                    if "-" in era:
                        era = 0
                    whip = split['stat']['whip']
                    if "-" in whip:
                        whip = 0
                    strikeoutWalkRatio = split['stat']['strikeoutWalkRatio']
                    games_started = split['stat']['gamesStarted']
                    hitsPer9Inn = split['stat']['hitsPer9Inn']
                    if "-" in hitsPer9Inn:
                        hitsPer9Inn = 0
                    strikeoutsPer9Inn = split['stat']['strikeoutsPer9Inn']
                    if "-" in strikeoutsPer9Inn:
                        strikeoutsPer9Inn = 0
                    walksPer9Inn = split['stat']['walksPer9Inn']
                    if "-" in walksPer9Inn:
                        walksPer9Inn = 0
                    strikeoutWalkRatio = stat.get("strikeoutWalkRatio")

    else:
        era = None
        whip = None
        strikeoutWalkRatio = None
        strikeoutWalkRatio = None
        games_started = None
        hitsPer9Inn = None
        strikeoutsPer9Inn = None
        walksPer9Inn = None

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO probablesStats (
            player_id, gameId, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (player_id, gamesId, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()