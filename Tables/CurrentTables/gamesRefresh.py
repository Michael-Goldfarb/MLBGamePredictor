import requests
import json
import psycopg2
from datetime import datetime

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()
games = data['dates'][0]['games']

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host='rajje.db.elephantsql.com',
    database='syabkhtb',
    user='syabkhtb',
    port='5432',
    password='J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gamesRefresh (
        gameId TEXT,
        awayTeamName VARCHAR(255),
        homeTeamName VARCHAR(255),
        gameStatus VARCHAR(255),
        gameDate DATE,
        gameTime TIME,
        awayTeamScore INTEGER,
        homeTeamScore INTEGER,
        awayTeamWinPct FLOAT,
        homeTeamWinPct FLOAT,
        venue VARCHAR(255),
        isWinnerAway BOOLEAN,
        isWinnerHome BOOLEAN,
        featuredWinner VARCHAR(255),
        correct BOOLEAN
    )
""")

# Get the total number of games played
totalGames = len(games)

# Initialize counters
numerator = 0
denominator = 0

records = []
for game in games:
    gameId = game['gamePk']
    awayTeamName = game['teams']['away']['team']['name']
    homeTeamName = game['teams']['home']['team']['name']
    gameStatus = game["status"]["detailedState"]
    gameDate = game['gameDate']
    gameTime = game['gameDate'][11:16]
    awayTeamScore = game['teams']['away'].get('score')
    homeTeamScore = game['teams']['home'].get('score')
    awayTeamWinPct = game["teams"]["away"]["leagueRecord"]["pct"]
    homeTeamWinPct = game["teams"]["home"]["leagueRecord"]["pct"]
    venue = game['venue']['name']
    isWinnerAway = game['teams']['away'].get('isWinner')
    isWinnerHome = game['teams']['home'].get('isWinner')
    
    # Retrieve the value of theWinner from the games table for the specific gameId
    cursor.execute("SELECT theWinner FROM games WHERE gameId = CAST(%s AS text);", (gameId,))
    theWinner = cursor.fetchone()[0]
    
    # Determine the correct value based on the conditions
    if isWinnerAway and awayTeamName == theWinner:
        correct = True
        numerator += 1
        denominator += 1
    elif isWinnerHome and homeTeamName == theWinner:
        correct = True
        numerator += 1
        denominator += 1
    elif isWinnerAway is None or isWinnerHome is None:
        correct = None
    else:
        correct = False
        denominator += 1
    print(correct)
    
    records.append((gameId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome, correct))

# Calculate the fraction of correct predictions
if denominator > 0:
    fraction_numerator = numerator
    fraction_denominator = denominator
else:
    fraction_numerator = None
    fraction_denominator = None

# Get the current date
currentDate = datetime.now().date()

# Delete the existing record for the current date if it exists
cursor.execute("DELETE FROM dailyPredictions WHERE prediction_date = %s", (currentDate,))

# Insert the daily prediction into the dailyPredictions table
cursor.execute("""
    INSERT INTO dailyPredictions (prediction_date, numerator, denominator)
    VALUES (%s, %s, %s)
""", (currentDate, fraction_numerator, fraction_denominator))




# Insert data into the table
cursor.execute("TRUNCATE TABLE gamesRefresh;")

if correct != None:
    cursor.executemany("""
        INSERT INTO gamesRefresh (gameId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, records)
else:
    cursor.executemany("""
        INSERT INTO gamesRefresh (gameId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome, correct)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, records)

cursor.execute("ALTER TABLE games ADD COLUMN IF NOT EXISTS correct BOOLEAN;")

# Update the 'correct' column in the games table
cursor.executemany("""
    UPDATE games
    SET correct = %s
    WHERE gameId = CAST(%s AS text)
""", [(correct, gameId) for gameId, *_ in records])

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
