import requests
import json
import psycopg2
from datetime import datetime

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()
games = data['dates'][0]['games']

records = []
for game in games:
    gameId = game['gamePk']
    awayTeamId = game['teams']['away']['team']['id']
    homeTeamId = game['teams']['home']['team']['id']
    awayTeamName = game['teams']['away']['team']['name']
    homeTeamName = game['teams']['home']['team']['name']

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
# Create the "LineupAndProbables" table (if it doesn't exist)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS LineupAndProbables (
        awayId INTEGER,
        awayName TEXT,
        homeId INTEGER,
        homeName TEXT,
        batterOneAway INTEGER,
        batterTwoAway INTEGER,
        batterThreeAway INTEGER,
        batterFourAway INTEGER,
        batterFiveAway INTEGER,
        batterSixAway INTEGER,
        batterSevenAway INTEGER,
        batterEightAway INTEGER,
        batterNineAway INTEGER,
        batterOneHome INTEGER,
        batterTwoHome INTEGER,
        batterThreeHome INTEGER,
        batterFourHome INTEGER,
        batterFiveHome INTEGER,
        batterSixHome INTEGER,
        batterSevenHome INTEGER,
        batterEightHome INTEGER,
        batterNineHome INTEGER,
        pitcherIdHome TEXT,
        pitcherIdAway TEXT,
        pitcherNameHome TEXT,
        pitcherNameAway TEXT
    );
""")  

# Truncate the table before inserting new data
cursor.execute("TRUNCATE TABLE LineupAndProbables;")

unique_games = []
game_ids = set()

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
    awayTeam = data['gameData']['teams']['away']
    homeTeam = data['gameData']['teams']['home']

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
    probablePitcherAway = data['gameData']['probablePitchers']['away']
    probablePitcherAwayId = data['gameData']['probablePitchers']['away']['id']

    # Check if battingOrderAway has at least 9 elements
    if len(battingOrderAway) >= 9:
        batterOneAway = battingOrderAway[0]
        batterTwoAway = battingOrderAway[1]
        batterThreeAway = battingOrderAway[2]
        batterFourAway = battingOrderAway[3]
        batterFiveAway = battingOrderAway[4]
        batterSixAway = battingOrderAway[5]
        batterSevenAway = battingOrderAway[6]
        batterEightAway = battingOrderAway[7]
        batterNineAway = battingOrderAway[8]
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
        batterTwoHome = battingOrderHome[1]
        batterThreeHome = battingOrderHome[2]
        batterFourHome = battingOrderHome[3]
        batterFiveHome = battingOrderHome[4]
        batterSixHome = battingOrderHome[5]
        batterSevenHome = battingOrderHome[6]
        batterEightHome = battingOrderHome[7]
        batterNineHome = battingOrderHome[8]
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

    # Insert the data into the "LineupAndProbables" table
    cursor.execute("""
        INSERT INTO LineupAndProbables (
        awayId, awayName, homeId, homeName, batterOneAway, batterTwoAway, batterThreeAway, batterFourAway, batterFiveAway,
        batterSixAway, batterSevenAway, batterEightAway, batterNineAway, batterOneHome, batterTwoHome, batterThreeHome, batterFourHome, 
        batterFiveHome, batterSixHome, batterSevenHome, batterEightHome, batterNineHome, pitcherIdHome, pitcherIdAway, pitcherNameHome, 
        pitcherNameAway
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """,
    (
        awayTeam['id'], awayTeam['name'], homeTeam['id'], homeTeam['name'], batterOneAway, batterTwoAway, batterThreeAway, batterFourAway,
        batterFiveAway, batterSixAway, batterSevenAway, batterEightAway, batterNineAway, batterOneHome, batterTwoHome, batterThreeHome,
        batterFourHome, batterFiveHome, batterSixHome, batterSevenHome, batterEightHome, batterNineHome,
        probablePitcherHome['id'], probablePitcherAway['id'], probablePitcherHome['fullName'], probablePitcherAway['fullName']
    ))


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()