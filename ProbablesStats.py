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
lineup = []
teamsLineup = []
teamsStarters = []
response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()
games = data['dates'][0]['games']

# Loop through each gameId and create rows in the "LineupAndProbables" table
for game in games:
    gameId = game['gamePk']
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

    probablePitcherHome = data['gameData']['probablePitchers']['home']
    probablePitcherHomeId = data['gameData']['probablePitchers']['home']['id']
    starters.append(probablePitcherHomeId)
    teamsStarters.append(homeTeamName)
    probablePitcherAway = data['gameData']['probablePitchers']['away']
    probablePitcherAwayId = data['gameData']['probablePitchers']['away']['id']
    starters.append(probablePitcherAwayId)
    teamsStarters.append(awayTeamName)

    # Check if battingOrderAway has at least 9 elements
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




# TODO - Create a table that shows individual stats - such as the starting pitchers stats, the individual batters in the lineup stats, etc.
# so for every player in game - return their pitching stats
# get pitching stats from https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2023&group=pitching&startDate=03/30/2023&endDate={currentDate}&leagueListId=mlb_milb
currentDate = datetime.now().strftime("%m/%d/%Y")

# Define the SQL statement to create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS probablesStats (
        player_id TEXT,
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
            # else:
            #     # Handle the case where 'splits' field is empty
            #     strikeoutWalkRatio = None
            #     games_started = None
            #     hitsPer9Inn = None
            #     strikeoutsPer9Inn = None
            #     era = None
            #     whip = None
            #     walksPer9Inn = None
    
    # if mlb_stat is not None:
    #     era = mlb_stat['era']
    #     whip = mlb_stat['whip']
    #     strikeoutWalkRatio = mlb_stat['strikeoutWalkRatio']
    #     games_started = mlb_stat['games_started']
    #     hitsPer9Inn = mlb_stat['hitsPer9Inn']
    #     strikeoutsPer9Inn = mlb_stat['strikeoutsPer9Inn']
    #     walksPer9Inn = mlb_stat['walksPer9Inn']
    # else:
    #     print("No MLB stats found.")
    
    

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO probablesStats (
            player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn))


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
