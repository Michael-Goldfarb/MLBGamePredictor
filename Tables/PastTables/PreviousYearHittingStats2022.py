import requests
import json
import psycopg2
from datetime import datetime
from requests.exceptions import SSLError
from requests.exceptions import ConnectionError
import time
import os

# TABLE WITH LAST YEARS STATS -- USE THIS TABLE IF GAMES PLAYED IS LESS THAN 5

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

lineup = []
teamsLineup = []
dates = []
gameIdss = []
outcomes = []
gamess = []

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-04-20&endDate=2022-10-01")
data = response.json()

i = 0
# Loop through each gameId
for date_info in data["dates"]:
    for game in date_info["games"]:
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
            gameIdss.append(gameId)
        awayTeamName = game['teams']['away']['team']['name']
        homeTeamName = game['teams']['home']['team']['name']
        isWinnerAway = game['teams']['away'].get('isWinner')
        if isWinnerAway is not None:
            for _ in range(9):
                outcomes.append(isWinnerAway)
        else:
            for _ in range(9):
                outcomes.append(None)
        isWinnerHome = game['teams']['home'].get('isWinner')
        if isWinnerHome is not None:
            for _ in range(9):
                outcomes.append(isWinnerHome)
        else:
            for _ in range(9):
                outcomes.append(None)
        if i == 0: # uses the first game twice for some reason
            i += 1
            continue
        if gameId == 663466: # all star game
            continue
        url = f"https://statsapi.mlb.com/api/v1.1/game/{game['gamePk']}/feed/live"
        response = requests.get(url)
        data = response.json()

        awayTeamName = data['gameData']['teams']['away']['id']
        homeTeamName = data['gameData']['teams']['home']['id']

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
    CREATE TABLE IF NOT EXISTS previousYearHittingStats2022v3 (
        date DATE,
        teamId TEXT,
        gameId TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        games_played INTEGER,
        babip TEXT,
        isWinner BOOLEAN
    );
""")
               
# Clear the table before inserting new data
cursor.execute("TRUNCATE TABLE previousYearHittingStats2022v3;")

obp = None
slg = None
ops = None
at_bats_per_home_run = None
games_played = 0
babip = None
team_stats = {}
# Iterate over the lineup
for index, playerId in enumerate(lineup):
    teamId = teamsLineup[index]  # Get the team id corresponding to the current player
    gameId = gameIdss[index]
    isWinner = outcomes[index]
    try:
        api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&group=hitting&startDate=07/24/2020&endDate=10/03/2021&leagueListId=mlb_milb".format(
            playerId=playerId,
        )
        theDate = dates[index]
        print(theDate)
        response = requests.get(api_url)
        data = response.json()
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
                        games_played = int(stat.get("gamesPlayed")) if stat.get("gamesPlayed") is not None else 0
                        obp = float(stat.get("obp")) if stat.get("obp") is not None else 0.0
                        slg = float(stat.get("slg")) if stat.get("slg") is not None else 0.0
                        ops = float(stat.get("ops")) if stat.get("ops") is not None else 0.0
                        babip = float(stat.get("babip")) if (stat.get("babip") is not None and stat.get("babip") != ".---") else 0.0
                        at_bats_per_home_run = float(stat.get("atBatsPerHomeRun")) if (stat.get("atBatsPerHomeRun") is not None and stat.get("atBatsPerHomeRun") != "-.--") else 0.0
                else:
                    # Handle the case where 'splits' field is empty
                    games_played = 0
                    obp = 0.0
                    slg = 0.0
                    ops = 0.0
                    at_bats_per_home_run = 0.0
                    babip = 0.0
            else:
                # Handle the case where 'stats' field is empty
                games_played = 0
                obp = 0.0
                slg = 0.0
                ops = 0.0
                at_bats_per_home_run = 0.0
                babip = 0.0
        else:
            # Handle the case where 'stats' field is missing
            games_played = 0
            obp = 0.0
            slg = 0.0
            ops = 0.0
            at_bats_per_home_run = 0.0
            babip = 0.0

        # Update the cumulative values for the current team
        team_game_key = (teamId, gameId)
        if team_game_key in team_stats:
            team_stats[team_game_key]["games_played"] += games_played
            team_stats[team_game_key]["obp"] += obp
            team_stats[team_game_key]["slg"] += slg
            team_stats[team_game_key]["ops"] += ops
            at_bats_per_home_run = float(stat.get("atBatsPerHomeRun")) if stat.get("atBatsPerHomeRun") != "-.--" else 0.0
            team_stats[team_game_key]["at_bats_per_home_run"] += at_bats_per_home_run
            team_stats[team_game_key]["babip"] += babip
        else:
            team_stats[team_game_key] = {
                "games_played": games_played,
                "obp": obp,
                "slg": slg,
                "ops": ops,
                "at_bats_per_home_run": at_bats_per_home_run,
                "babip": babip if babip is not None else 0.0
            }
            team_stats[team_game_key]["isWinner"] = isWinner
            team_stats[team_game_key]["date"] = theDate
    except (ConnectionResetError, ConnectionError) as e:
            # Handle the connection-related exception
            print(f"Connection error occurred: {e}")
            # Optionally, you can wait for some time before retrying
            time.sleep(1)  # Wait for 1 second before retrying the request
            continue
    
    except SSLError as e:
        print("SSL handshake failure occurred. Retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying
        continue  # Continue to the next iteration

while True:
    try:
        # Calculate the averages for each column per team
        for team_game_key, stats in team_stats.items():
            teamId, gameId = team_game_key
            num_players = 9  # Assuming lineup contains all players for each team
            games_played_avg = stats["games_played"] / num_players
            obp_avg = stats["obp"] / num_players
            slg_avg = stats["slg"] / num_players
            ops_avg = stats["ops"] / num_players
            at_bats_per_home_run_avg = stats["at_bats_per_home_run"] / num_players
            babip_avg = stats["babip"] / num_players
            isWinner = stats["isWinner"]
            dates = stats["date"]
            print(dates)

            # Insert the player stats into the table
            cursor.execute("""
                INSERT INTO previousYearHittingStats2022v3 (
                    date, gameId, teamId, obp, slg, ops, at_bats_per_home_run, games_played, babip, isWinner
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                dates, gameId, teamId, obp_avg, slg_avg, ops_avg, at_bats_per_home_run_avg, games_played_avg, babip_avg, isWinner
            ))

        break

    except psycopg2.Error as e:
        print("Error occurred during database insertion:", e)
        time.sleep(1)  # Wait for 1 second before retrying the request
        continue
    except (ConnectionResetError, ConnectionError) as e:
        # Handle the connection-related exception
        print(f"Connection error occurred: {e}")
        # Optionally, you can wait for some time before retrying
        time.sleep(1)  # Wait for 1 second before retrying the request
        continue
        
    except SSLError as e:
        print("SSL handshake failure occurred. Retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying
        continue  # Continue to the next iteration


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()