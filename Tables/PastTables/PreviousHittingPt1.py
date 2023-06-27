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
dates = []
gameIdss = []
outcomes = []

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-06-07&endDate=2022-07-07")
data = response.json()

i = 0
# Loop through each gameId
for date_info in data["dates"]:
    for game in date_info["games"]:
        print(game['gamePk'])
        gameId = game['gamePk']
        gameDate = game['officialDate']
        print(gameDate)
        for _ in range(18):
            dates.append(gameDate)
        awayTeamId = game['teams']['away']['team']['id']
        homeTeamId = game['teams']['home']['team']['id']
        if game['gamePk'] == "662183": # for some reason the away pitcher is not provided for this game
            continue
        for _ in range(18):
            gameIdss.append(gameDate)
        awayTeamName = game['teams']['away']['team']['name']
        homeTeamName = game['teams']['home']['team']['name']
        isWinnerAway = game['teams']['away'].get('isWinner')
        if isWinnerAway is not None:
            for _ in range(9):
                outcomes.append(isWinnerAway)
        else:
            for _ in range(9):
                outcomes.append(False)
        isWinnerHome = game['teams']['home'].get('isWinner')
        if isWinnerHome is not None:
            for _ in range(9):
                outcomes.append(isWinnerHome)
        else:
            for _ in range(9):
                outcomes.append(False)
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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pt1previousYearHittingStats2022 (
        player_id TEXT,
        gameId TEXT,
        player_name TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        team_name TEXT,
        games_played INTEGER,
        babip TEXT,
        isWinner BOOLEAN
    );
""")
               
# Clear the table before inserting new data
cursor.execute("TRUNCATE TABLE pt1previousYearHittingStats2022;")

obp = None
slg = None
ops = None
at_bats_per_home_run = None
games_played = None
babip = None
# Iterate over the lineup
for index, playerId in enumerate(lineup):
    team_name = teamsLineup[index]  # Get the team name corresponding to the current player
    theDate = dates[index]
    print(theDate)
    gameId = gameIdss[index]
    isWinner = outcomes[index]
    url = f"https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&group=hitting&startDate=07/24/2020&endDate=10/03/2021&leagueListId=mlb_milb"
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
        INSERT INTO pt1previousYearHittingStats2022 (
            player_id, gameId, player_name, obp, slg, ops, at_bats_per_home_run, team_name, games_played, babip, isWinner
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, gameId, player_name, obp, slg, ops, at_bats_per_home_run, team_name, games_played, babip, isWinner
    ))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
