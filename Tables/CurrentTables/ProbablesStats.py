import requests
import json
import psycopg2
from datetime import datetime

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
unique_games = []
game_ids = set()
starters = []
gameIdss = []
teamsStarters = []
startersName = []
response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()
games = data['dates'][0]['games']

# Loop through each gameId and create rows in the "LineupAndProbables" table
for game in games:
    gameId = game['gamePk']
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
    probablePitcherHome = data['gameData']['probablePitchers']['home']
    probablePitcherHomeId = data['gameData']['probablePitchers']['home']['id']
    starters.append(probablePitcherHomeId)
    startersName.append(probablePitcherHome['fullName'])
    teamsStarters.append(homeTeamName)
    probablePitcherAway = data['gameData']['probablePitchers']['away']
    probablePitcherAwayId = data['gameData']['probablePitchers']['away']['id']
    starters.append(probablePitcherAwayId)
    startersName.append(probablePitcherAway['fullName'])
    teamsStarters.append(awayTeamName)

# Define the SQL statement to create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS probablesStats (
        player_id TEXT,
        gameId TEXT,
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
    gamesId = gameIdss[index]

    # Make the API request to fetch player stats
    api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2023&group=pitching&startDate=03/30/2023&endDate={currentDate}&leagueListId=mlb_milb".format(
        playerId=player_id,
        currentDate=datetime.now().strftime("%m/%d/%Y")  
    )
    response = requests.get(api_url)
    data = response.json()
    for stat in data['stats']:
        for split in stat["splits"]:
            if split["sport"]["abbreviation"] == "MLB":
                era = split["stat"]["era"]
                whip = split['stat']['whip']
                strikeoutWalkRatio = split['stat']['strikeoutWalkRatio']
                strikeoutWalkRatio = split['stat']['strikeoutWalkRatio']
                games_started = split['stat']['gamesStarted']
                hitsPer9Inn = split['stat']['hitsPer9Inn']
                strikeoutsPer9Inn = split['stat']['strikeoutsPer9Inn']
                walksPer9Inn = split['stat']['walksPer9Inn']
    

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO probablesStats (
            player_id, gamesId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (player_id, gamesId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn))


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()