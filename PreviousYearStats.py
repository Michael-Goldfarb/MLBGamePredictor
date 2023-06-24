
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
lineup = []
teamsLineup = []
teamsStarters = []
game_ids = set()
unique_games = []

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



cursor.execute("""
    CREATE TABLE IF NOT EXISTS previousYearPitchingStats (
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
               
# Clear the table before inserting new data
cursor.execute("TRUNCATE TABLE previousYearPitchingStats;")

     # SEE IF THERE IS A DIFFERENCE IF IT IS A TEXT OR FLOAT

# Iterate over the starters
for index, playerId in enumerate(starters):
    team_name = teamsStarters[index]  # Get the team name corresponding to the current player
    url = f"https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2022&group=pitching&startDate=05/07/2022&endDate=10/05/2022&leagueListId=mlb_milb"
    response = requests.get(url)
    data = json.loads(response.text)
    player_id = playerId

    if 'stats' in data and data['stats']:
        # Check if the 'stats' field is present and not empty
        stats = data['stats'][0]['splits'][0]['stat']
        strikeoutWalkRatio = stats["strikeoutWalkRatio"]
        games_started = stats["gamesStarted"]
        hitsPer9Inn = stats["hitsPer9Inn"]
        strikeoutsPer9Inn = stats["strikeoutsPer9Inn"]
        era = stats["era"]
        whip = stats["whip"]
        walksPer9Inn = stats["walksPer9Inn"]
    else:
        # Set default values or handle the case where the required fields are missing
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
            player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
    ))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
