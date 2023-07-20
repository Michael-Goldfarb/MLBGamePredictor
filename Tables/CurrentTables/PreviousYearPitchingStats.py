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

starters = []
teamsStarters = []
starter = []
gameIdss = []
game_ids = set()
unique_games = []
teamsId = []

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
# response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-07-18&endDate=2023-07-18")
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

     # Check if 'home' exists in probablePitchers
    if 'home' in data['gameData']['probablePitchers']:
        probablePitcherHome = data['gameData']['probablePitchers']['home']
        starter.append(probablePitcherHome['fullName'])
        starters.append(probablePitcherHome['id'])
        teamsStarters.append(homeTeamName)
        teamsId.append(homeTeamId)

    # Check if 'away' exists in probablePitchers
    if 'away' in data['gameData']['probablePitchers']:
        probablePitcherAway = data['gameData']['probablePitchers']['away']
        starter.append(probablePitcherAway['fullName'])
        starters.append(probablePitcherAway['id'])
        teamsStarters.append(awayTeamName)
        teamsId.append(awayTeamId)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS previousYearPitchingStats (
        player_id TEXT,
        gameId TEXT,
        teamId TEXT,
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
               
# Clear the table before inserting new data
cursor.execute("TRUNCATE TABLE previousYearPitchingStats;")

strikeoutWalkRatio = None
games_started = None
hitsPer9Inn = None
strikeoutsPer9Inn = None
era = None
whip = None
walksPer9Inn = None
# Iterate over the starters
for index, playerId in enumerate(starters):
    team_name = teamsStarters[index]  # Get the team name corresponding to the current player
    player_name = starter[index]
    teamId = teamsId[index]
    print(player_name)
    gamesId = gameIdss[index]
    print(gamesId)
    url = f"https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&group=pitching&startDate=05/01/2021&endDate=10/05/2022&leagueListId=mlb_milb"
    response = requests.get(url)
    data = json.loads(response.text)
    player_id = playerId
    if 'stats' in data and data['stats']:
        stats_list = data['stats']
        if stats_list:
            last_stats = stats_list[-1]  # Get the last instance of 'stats'
            if 'splits' in last_stats and last_stats['splits']:
                splits = last_stats['splits']
                last_split = splits[-1]  # Get the last instance of 'splits'
                if 'stat' in last_split:
                    stat = last_split['stat']
                    # Retrieve the required fields and handle "-" values
                    strikeoutWalkRatio = stat.get("strikeoutWalkRatio")
                    if "-" in strikeoutWalkRatio:
                        strikeoutWalkRatio = 0
                    games_started = stat.get("gamesStarted")
                    if games_started is not None and "-" in str(games_started):
                        games_started = 0
                    hitsPer9Inn = stat.get("hitsPer9Inn")
                    if "-" in hitsPer9Inn:
                        hitsPer9Inn = 0
                    strikeoutsPer9Inn = stat.get("strikeoutsPer9Inn")
                    if "-" in strikeoutsPer9Inn:
                        strikeoutsPer9Inn = 0
                    era = stat.get("era")
                    if "-" in era:
                        era = 0
                    whip = stat.get("whip")
                    if "-" in whip:
                        whip = 0
                    walksPer9Inn = stat.get("walksPer9Inn")
                    if "-" in walksPer9Inn:
                        walksPer9Inn = 0
    else:
        # Handle the case where 'stats' field is missing
        strikeoutWalkRatio = None
        games_started = None
        hitsPer9Inn = None
        strikeoutsPer9Inn = None
        era = None
        whip = None
        walksPer9Inn = None

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO previousYearPitchingStats (
            player_id, gameId, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, gamesId, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
    ))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()