import requests
import json
import psycopg2
from datetime import datetime

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-06-07&endDate=2022-08-07")
data = response.json()

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
# Create the "LineupAndProbables2022" table (if it doesn't exist)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS LineupAndProbables2022 (
        gameDate DATE,
        gameId TEXT,
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
        pitcherNameAway TEXT,
        isWinnerAway BOOLEAN,
        isWinnerHome BOOLEAN
    );
""")  

# Truncate the table before inserting new data
cursor.execute("TRUNCATE TABLE LineupAndProbables2022;")

# Loop through each gameId and create rows in the "LineupAndProbables2022" table
i = 0
for date_info in data["dates"]:
    for game in date_info["games"]:
        gameId = game['gamePk']
        gameDate = game['officialDate']
        print(gameDate)
        awayTeamId = game['teams']['away']['team']['id']
        homeTeamId = game['teams']['home']['team']['id']
        awayTeamName = game['teams']['away']['team']['name']
        homeTeamName = game['teams']['home']['team']['name']
        isWinnerAway = game['teams']['away'].get('isWinner')
        isWinnerHome = game['teams']['home'].get('isWinner')
        if game['gamePk'] == "662183": # for some reason the away pitcher is not provided for this game
            continue
        if i == 0: # uses the first game twice for some reason
            i += 1
            continue
        if gameId == 663466: # all star game
            continue
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
        probablePitcherAway = data['gameData']['probablePitchers'].get('away')  # Use get() method to handle missing key
        print(probablePitcherHome['fullName'])
        if probablePitcherAway is not None:
            probablePitcherAway = data['gameData']['probablePitchers']['away']
            probablePitcherAwayId = data['gameData']['probablePitchers']['away']['id']
            probablePitcherAwayName = data['gameData']['probablePitchers']['away']['fullName']
        
        batterOneAway = battingOrderAway[0]
        batterTwoAway = battingOrderAway[1]
        batterThreeAway = battingOrderAway[2]
        batterFourAway = battingOrderAway[3]
        batterFiveAway = battingOrderAway[4]
        batterSixAway = battingOrderAway[5]
        batterSevenAway = battingOrderAway[6]
        batterEightAway = battingOrderAway[7]
        batterNineAway = battingOrderAway[8]

        batterOneHome = battingOrderHome[0]
        batterTwoHome = battingOrderHome[1]
        batterThreeHome = battingOrderHome[2]
        batterFourHome = battingOrderHome[3]
        batterFiveHome = battingOrderHome[4]
        batterSixHome = battingOrderHome[5]
        batterSevenHome = battingOrderHome[6]
        batterEightHome = battingOrderHome[7]
        batterNineHome = battingOrderHome[8]
        print(batterNineHome)

        # Insert the data into the "LineupAndProbables2022" table
        cursor.execute("""
            INSERT INTO LineupAndProbables2022 (
            gameDate, gameId, awayId, awayName, homeId, homeName, batterOneAway, batterTwoAway, batterThreeAway, batterFourAway, batterFiveAway,
            batterSixAway, batterSevenAway, batterEightAway, batterNineAway, batterOneHome, batterTwoHome, batterThreeHome, batterFourHome, 
            batterFiveHome, batterSixHome, batterSevenHome, batterEightHome, batterNineHome, pitcherIdHome, pitcherIdAway, pitcherNameHome, 
            pitcherNameAway, isWinnerAway, isWinnerHome
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            gameDate, gameId, awayTeam['id'], awayTeam['name'], homeTeam['id'], homeTeam['name'], batterOneAway, batterTwoAway, batterThreeAway, batterFourAway,
            batterFiveAway, batterSixAway, batterSevenAway, batterEightAway, batterNineAway, batterOneHome, batterTwoHome, batterThreeHome,
            batterFourHome, batterFiveHome, batterSixHome, batterSevenHome, batterEightHome, batterNineHome,
            probablePitcherHome['id'], probablePitcherAwayId, probablePitcherHome['fullName'], probablePitcherAwayName, isWinnerAway, isWinnerHome
        ))


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()