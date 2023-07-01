import requests
import json
import psycopg2
from datetime import datetime

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host='rajje.db.elephantsql.com',
    database='syabkhtb',
    user='syabkhtb',
    port='5432',
    password='J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()

lineup = []
teamsLineup = []
gameIdss = []

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()
games = data['dates'][0]['games']

# Loop through each gameId and create rows in the "LineupAndProbables" table
for game in games:
    gamesId = game['gamePk']
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

    # Check if battingOrderAway has at least 9 elements
    # Can make this less code
    if len(battingOrderAway) >= 9:
        batterOneAway = battingOrderAway[0]
        lineup.append(battingOrderAway[0])
        for _ in range(9):
            teamsLineup.append(awayTeamName)
            gameIdss.append(gamesId)
        batterTwoAway = battingOrderAway[1]
        lineup.append(battingOrderAway[1])
        batterThreeAway = battingOrderAway[2]
        lineup.append(battingOrderAway[2])
        batterFourAway = battingOrderAway[3]
        lineup.append(battingOrderAway[3])
        batterFiveAway = battingOrderAway[4]
        lineup.append(battingOrderAway[4])
        batterSixAway = battingOrderAway[5]
        lineup.append(battingOrderAway[5])
        batterSevenAway = battingOrderAway[6]
        lineup.append(battingOrderAway[6])
        batterEightAway = battingOrderAway[7]
        lineup.append(battingOrderAway[7])
        batterNineAway = battingOrderAway[8]
        lineup.append(battingOrderAway[8])
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
        for _ in range(9):
            teamsLineup.append(homeTeamName)
            gameIdss.append(gamesId)
        batterTwoHome = battingOrderHome[1]
        lineup.append(battingOrderHome[1])
        batterThreeHome = battingOrderHome[2]
        lineup.append(battingOrderHome[2])
        batterFourHome = battingOrderHome[3]
        lineup.append(battingOrderHome[3])
        batterFiveHome = battingOrderHome[4]
        lineup.append(battingOrderHome[4])
        batterSixHome = battingOrderHome[5]
        lineup.append(battingOrderHome[5])
        batterSevenHome = battingOrderHome[6]
        lineup.append(battingOrderHome[6])
        batterEightHome = battingOrderHome[7]
        lineup.append(battingOrderHome[7])
        batterNineHome = battingOrderHome[8]
        lineup.append(battingOrderHome[8])
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
        gameId TEXT,
        teamId TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        games_played INTEGER,
        babip TEXT
    );
""")

# Clear the table before inserting new data
cursor.execute("TRUNCATE TABLE previousYearHittingStats;")

team_stats = {}

# Make the API request to fetch player stats and insert into the table
for index, playerId in enumerate(lineup):
    teamId = teamsLineup[index]  # Get the team name corresponding to the current player
    gameId = gameIdss[index]

    # Make the API request to fetch player stats
    api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2023&group=hitting&startDate=03/30/2023&endDate={currentDate}&leagueListId=mlb_milb".format(
        playerId=playerId,
        currentDate=datetime.now().strftime("%m/%d/%Y")
    )
    response = requests.get(api_url)
    data = response.json()

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
                    games_played = int(stat.get("gamesPlayed"))
                    obp = float(stat.get("obp"))
                    slg = float(stat.get("slg"))
                    ops = float(stat.get("ops"))
                    babip = float(stat.get("babip")) if stat.get("babip") != ".---" else 0.0
                    if stat.get("atBatsPerHomeRun") != "-.--":
                        at_bats_per_home_run = float(stat.get("atBatsPerHomeRun"))
                    else:
                        at_bats_per_home_run = 0.0
            else:
                # Handle the case where 'splits' field is empty
                games_played = None
                obp = None
                slg = None
                ops = None
                at_bats_per_home_run = None
                babip = None
        else:
            # Handle the case where 'stats' field is empty
            games_played = None
            obp = None
            slg = None
            ops = None
            at_bats_per_home_run = None
            babip = None
    else:
        # Handle the case where 'stats' field is missing
        games_played = None
        obp = None
        slg = None
        ops = None
        at_bats_per_home_run = None
        babip = None

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
        # Create a new entry in the team_stats dictionary for the current team
        team_stats[team_game_key] = {
            "games_played": games_played,
            "obp": obp,
            "slg": slg,
            "ops": ops,
            "at_bats_per_home_run": at_bats_per_home_run,
            "babip": babip,
        }

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

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO previousYearHittingStats (
            gameId, teamId, obp, slg, ops, at_bats_per_home_run, games_played, babip
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        gameId, teamId, obp_avg, slg_avg, ops_avg, at_bats_per_home_run_avg, games_played_avg, babip_avg
    ))

# Commit the changes to the database
conn.commit()

# Close the database connection
cursor.close()
conn.close()
