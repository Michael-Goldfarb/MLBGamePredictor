import requests
import json
import psycopg2
from datetime import datetime

# TABLE WITH LAST YEARS STATS -- USE THIS TABLE IF GAMES PLAYED IS LESS THAN 5

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()

lineup = []
teamsLineup = []
gameIdss = []
game_ids = set()
unique_games = []

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

    # Parse battingOrder if it is a string representation of an array
    battingOrderHome_str = data['liveData']['boxscore']['teams']['home'].get('battingOrder')
    if isinstance(battingOrderHome_str, str):
        battingOrderHome = json.loads(battingOrderHome_str)
    else:
        battingOrderHome = battingOrderHome_str

    battingOrderAway_str = data['liveData']['boxscore']['teams']['away'].get('battingOrder')
    if isinstance(battingOrderAway_str, str):
        battingOrderAway = json.loads(battingOrderAway_str)
    else:
        battingOrderAway = battingOrderAway_str

    # Check if battingOrderAway has at least 9 elements
    # Can make this less code
    if len(battingOrderAway) >= 9:
        batterOneAway = battingOrderAway[0]
        lineup.append(battingOrderAway[0])
        teamsLineup.append(awayTeamName)
        batterTwoAway = battingOrderAway[1]
        lineup.append(battingOrderAway[1])
        teamsLineup.append(awayTeamName)
        batterThreeAway = battingOrderAway[2]
        lineup.append(battingOrderAway[2])
        teamsLineup.append(awayTeamName)
        batterFourAway = battingOrderAway[3]
        lineup.append(battingOrderAway[3])
        teamsLineup.append(awayTeamName)
        batterFiveAway = battingOrderAway[4]
        lineup.append(battingOrderAway[4])
        teamsLineup.append(awayTeamName)
        batterSixAway = battingOrderAway[5]
        lineup.append(battingOrderAway[5])
        teamsLineup.append(awayTeamName)
        batterSevenAway = battingOrderAway[6]
        lineup.append(battingOrderAway[6])
        teamsLineup.append(awayTeamName)
        batterEightAway = battingOrderAway[7]
        lineup.append(battingOrderAway[7])
        teamsLineup.append(awayTeamName)
        batterNineAway = battingOrderAway[8]
        lineup.append(battingOrderAway[8])
        teamsLineup.append(awayTeamName)
    else:
        # Set default values or handle the case where there are not enough elements
        batterOneAway = None
        batterTwoAway = None
        batterThreeAway = None
        batterFourAway = None
        batterFiveAway = None
        batterSixAway = None
        batterSevenAway = None
        batterEightAway = None
        batterNineAway = None

    # Check if battingOrderHome has at least 9 elements
    if len(battingOrderHome) >= 9:
        batterOneHome = battingOrderHome[0]
        lineup.append(battingOrderHome[0])
        teamsLineup.append(homeTeamName)
        batterTwoHome = battingOrderHome[1]
        lineup.append(battingOrderHome[1])
        teamsLineup.append(homeTeamName)
        batterThreeHome = battingOrderHome[2]
        lineup.append(battingOrderHome[2])
        teamsLineup.append(homeTeamName)
        batterFourHome = battingOrderHome[3]
        lineup.append(battingOrderHome[3])
        teamsLineup.append(homeTeamName)
        batterFiveHome = battingOrderHome[4]
        lineup.append(battingOrderHome[4])
        teamsLineup.append(homeTeamName)
        batterSixHome = battingOrderHome[5]
        lineup.append(battingOrderHome[5])
        teamsLineup.append(homeTeamName)
        batterSevenHome = battingOrderHome[6]
        lineup.append(battingOrderHome[6])
        teamsLineup.append(homeTeamName)
        batterEightHome = battingOrderHome[7]
        lineup.append(battingOrderHome[7])
        teamsLineup.append(homeTeamName)
        batterNineHome = battingOrderHome[8]
        lineup.append(battingOrderHome[8])
        teamsLineup.append(homeTeamName)
    else:
        # Set default values or handle the case where there are not enough elements
        batterOneHome = None
        batterTwoHome = None
        batterThreeHome = None
        batterFourHome = None
        batterFiveHome = None
        batterSixHome = None
        batterSevenHome = None
        batterEightHome = None
        batterNineHome = None


cursor.execute("""
    CREATE TABLE IF NOT EXISTS previousYearHittingStats (
        player_id TEXT,
        gamesId TEXT,
        player_name TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        team_name TEXT,
        games_played INTEGER,
        babip TEXT,
    );
""")
               
# Clear the table before inserting new data
cursor.execute("TRUNCATE TABLE previousYearHittingStats;")

obp = None
slg = None
ops = None
at_bats_per_home_run = None
games_played = None
babip = None
# Iterate over the lineup
for index, playerId in enumerate(lineup):
    team_name = teamsLineup[index]  # Get the team name corresponding to the current player
    gamesId = gameIdss[index]
    url = f"https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&group=hitting&startDate=05/01/2021&endDate=10/05/2022&leagueListId=mlb_milb"
    response = requests.get(url)
    data = json.loads(response.text)
    player_id = playerId
    api_url2 = "https://statsapi.mlb.com/api/v1/people/{playerId2}".format(
        playerId2 = player_id,
    )
    response2 = requests.get(api_url2)
    data2 = response2.json()
    player_name = data2["people"][0]["fullName"]
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
                    obp = stat.get("obp")
                    slg = stat.get("slg")
                    ops = stat.get("ops")
                    at_bats_per_home_run = stat.get("atBatsPerHomeRun")
                    games_played = stat.get("gamesPlayed")
                    babip = stat.get("babip")
            else:
                # Handle the case where 'splits' field is empty
                obp = None
                slg = None
                ops = None
                at_bats_per_home_run = None
                games_played = None
                babip = None
        else:
            # Handle the case where 'stats' field is empty
            obp = None
            slg = None
            ops = None
            at_bats_per_home_run = None
            games_played = None
            babip = None
    else:
        # Handle the case where 'stats' field is missing
        obp = None
        slg = None
        ops = None
        at_bats_per_home_run = None
        games_played = None
        babip = None

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO previousYearHittingStats (
            player_id, gamesId, player_name, obp, slg, ops, at_bats_per_home_run, team_name, games_played, babip
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, gamesId, player_name, obp, slg, ops, at_bats_per_home_run, team_name, games_played, babip
    ))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
