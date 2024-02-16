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
dates = []
gameIdss = []
outcomes = []
teamIdss = []

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-03-30&endDate=2023-10-01")
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
        if gameId == 717421: # all star game
            continue
        url = f"https://statsapi.mlb.com/api/v1.1/game/{game['gamePk']}/feed/live"
        response = requests.get(url)
        data = response.json()
        awayTeamName = data['gameData']['teams']['away']['name']
        homeTeamName = data['gameData']['teams']['home']['name']
        awayTeamId = data['gameData']['teams']['away']['id']
        homeTeamId = data['gameData']['teams']['home']['id']
        probablePitcherHome = data['gameData']['probablePitchers']['home']
        starter.append(probablePitcherHome['fullName'])
        starters.append(probablePitcherHome['id'])
        teamsStarters.append(homeTeamName)
        teamIdss.append(homeTeamId)
        probablePitcherAway = data['gameData']['probablePitchers'].get('away')  # Use get() method to handle missing key
        print(probablePitcherHome['fullName'])
        if probablePitcherAway is not None:
            starter.append(probablePitcherAway['fullName'])
            starters.append(probablePitcherAway['id'])
            teamsStarters.append(awayTeamName)
            teamIdss.append(awayTeamId)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS previousYearPitchingStats2022V3 (
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

    cursor.execute("TRUNCATE TABLE previousYearPitchingStats2022V3;")

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
    game_ids = gameIdss[index]
    theDate = dates[index]
    teamId = teamIdss[index]
    isWinner = outcomes[index]
     #   game_date = dates[index]
    url = f"https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&group=pitching&startDate=04/01/2021&endDate=10/01/2022&leagueListId=mlb_milb"
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
                    print(whip)
                    walksPer9Inn = stat.get("walksPer9Inn")
            else:
            # Handle the case where 'splits' field is empty
                strikeoutWalkRatio = None
                games_started = None
                hitsPer9Inn = None
                strikeoutsPer9Inn = None
                era = None
                whip = None
                walksPer9Inn = None
        else:
            # Handle the case where 'stats' field is empty
            strikeoutWalkRatio = None
            games_started = None
            hitsPer9Inn = None
            strikeoutsPer9Inn = None
            era = None
            whip = None
            walksPer9Inn = None
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
        INSERT INTO previousYearPitchingStats2022V3 (
            player_id, gameDate, gameId, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn, isWinner
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, theDate, game_ids, teamId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn, isWinner
    ))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()