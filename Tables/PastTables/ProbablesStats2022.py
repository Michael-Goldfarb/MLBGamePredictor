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
starter = []
teamsStarters = []
startersName = []
dates = []
gameIdss = []
outcomes = []
teamIdss = []

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-04-20&endDate=2022-10-01")
data = response.json()

i = 0
# Loop through each gameId
for date_info in data["dates"]:
    for game in date_info["games"]:
        print(game['gamePk'])
        gameId = game['gamePk']
        gameDate = game['officialDate']
        print(gameDate)
        awayTeamId = game['teams']['away']['team']['id']
        homeTeamId = game['teams']['home']['team']['id']
        if game['gamePk'] == "662183": # for some reason the away pitcher is not provided for this game
            continue
        gameIdss.append(gameId)
        gameIdss.append(gameId)
        dates.append(gameDate)
        dates.append(gameDate)
        awayTeamName = game['teams']['away']['team']['name']
        homeTeamName = game['teams']['home']['team']['name']
        isWinnerHome = game['teams']['home'].get('isWinner')
        if isWinnerHome is not None:
            outcomes.append(isWinnerHome)
        else:
            outcomes.append(None) 
        isWinnerAway = game['teams']['away'].get('isWinner')
        if isWinnerAway is not None:
            outcomes.append(isWinnerAway)
        else:
            outcomes.append(None) 
        if i == 0: # uses the first game twice for some reason
            i += 1
            continue
        if gameId == 663466: # all star game
            continue
        url = f"https://statsapi.mlb.com/api/v1.1/game/{game['gamePk']}/feed/live"
        response = requests.get(url)
        data = response.json()
        awayTeamName = data['gameData']['teams']['away']['name']
        homeTeamName = data['gameData']['teams']['home']['name']
        homeTeamId = data['gameData']['teams']['home']['id']
        awayTeamId = data['gameData']['teams']['away']['id']
        probablePitcherHome = data['gameData']['probablePitchers']['home']
        startersName.append(probablePitcherHome['fullName'])
        starters.append(probablePitcherHome['id'])
        teamsStarters.append(homeTeamName)
        teamIdss.append(homeTeamId)
        probablePitcherAway = data['gameData']['probablePitchers'].get('away')  # Use get() method to handle missing key
        print(probablePitcherHome['fullName'])
        if probablePitcherAway is not None:
            startersName.append(probablePitcherAway['fullName'])
            starters.append(probablePitcherAway['id'])
            teamIdss.append(homeTeamId)
            teamsStarters.append(awayTeamName)

# Define the SQL statement to create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS probablesStats2022V3 (
            player_id TEXT,
            gameDate DATE,
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
            walksPer9Inn TEXT,
            isWinner BOOLEAN
    );
""")

# Truncate the table before inserting new data
cursor.execute("TRUNCATE TABLE probablesStats2022V3;")

for index, player_id in enumerate(starters):
    team_name = teamsStarters[index]  # Get the team name corresponding to the current player
    player_name = startersName[index]
    isWinner = outcomes[index]
    theDate = dates[index]
    print(theDate)
    game_ids = gameIdss[index]
    teamId = teamIdss[index]

    # Make the API request to fetch player stats
    api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2022&group=pitching&startDate=04/07/2022&endDate={currentDate}&leagueListId=mlb_milb".format(
        playerId=player_id,
        currentDate= dates[index]
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
        INSERT INTO probablesStats2022V3 (
           player_id, gameDate, gameId, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn, isWinner
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (player_id, theDate, game_ids, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn, isWinner))


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()