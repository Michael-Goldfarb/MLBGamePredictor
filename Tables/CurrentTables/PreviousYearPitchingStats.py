import requests
import json
import psycopg2
from datetime import datetime

# TABLE WITH LAST YEARS STATS -- USE THIS TABLE IF GAMES_STARTED IS LESS THAN 5

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
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
data = response.json()
games = data['dates'][0]['games']


# Loop through each gameId and create rows in the "LineupAndProbables" table
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
                    # Retrieve the required fields
                    strikeoutWalkRatio = stat.get("strikeoutWalkRatio")
                    games_started = stat.get("gamesStarted")
                    hitsPer9Inn = stat.get("hitsPer9Inn")
                    strikeoutsPer9Inn = stat.get("strikeoutsPer9Inn")
                    era = stat.get("era")
                    whip = stat.get("whip")
                    walksPer9Inn = stat.get("walksPer9Inn")
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