import requests
import json
import psycopg2
from datetime import datetime

# MAKE ANOTHER TABLE WITH LAST YEARS STATS -- USE THIS TABLE IF GAMES_STARTED IS LESS THAN 5

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
dates = []
gameIdss = []

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-06-07&endDate=2022-08-07")
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
        isWinnerAway = game['teams']['away'].get('isWinner')
        isWinnerHome = game['teams']['home'].get('isWinner')
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
        probablePitcherHome = data['gameData']['probablePitchers']['home']
        starter.append(probablePitcherHome['fullName'])
        starters.append(probablePitcherHome['id'])
        teamsStarters.append(homeTeamName)
        probablePitcherAway = data['gameData']['probablePitchers'].get('away')  # Use get() method to handle missing key
        print(probablePitcherHome['fullName'])
        if probablePitcherAway is not None:
            starter.append(probablePitcherAway['fullName'])
            starters.append(probablePitcherAway['id'])
            teamsStarters.append(awayTeamName)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS previousYearPitchingStats2022 (
            player_id TEXT,
            gameDate DATE,
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

    cursor.execute("TRUNCATE TABLE PreviousYearPitchingStats2022;")

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
     #   game_date = dates[index]
    url = f"https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&group=pitching&startDate=07/24/2020&endDate=10/03/2021&leagueListId=mlb_milb"
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
        INSERT INTO previousYearPitchingStats2022 (
            player_id, gameDate, gameId, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, theDate, game_ids, player_name, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
    ))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()