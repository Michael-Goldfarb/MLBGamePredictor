import requests
import json
import psycopg2
from datetime import datetime


response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
# response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-07-18&endDate=2023-07-18")
data = response.json()
games = data['dates'][0]['games']

records = []
for game in games:
    gameId = game['gamePk']
    awayTeamId = game['teams']['away']['team']['id']
    homeTeamId = game['teams']['home']['team']['id']
    awayTeamName = game['teams']['away']['team']['name']
    homeTeamName = game['teams']['home']['team']['name']
    awayTeamScore = game['teams']['away'].get('score')
    homeTeamScore = game['teams']['home'].get('score')
    awayTeamWinPct = game["teams"]["away"]["leagueRecord"]["pct"]
    homeTeamWinPct = game["teams"]["home"]["leagueRecord"]["pct"]
    # if it has ended, get a "isWinner" field to see who wins
    isWinnerAway = game['teams']['away'].get('isWinner')
    isWinnerHome = game['teams']['home'].get('isWinner')
    records.append((gameId, awayTeamId, homeTeamId, awayTeamName, homeTeamName, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, isWinnerAway, isWinnerHome))

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        gameId TEXT,
        awayTeamId INTEGER,
        homeTeamId INTEGER,
        awayTeamName VARCHAR(255),
        homeTeamName VARCHAR(255),
        awayTeamScore INTEGER,
        homeTeamScore INTEGER,
        awayTeamWinPct FLOAT,
        homeTeamWinPct FLOAT,
        isWinnerAway BOOLEAN,
        isWinnerHome BOOLEAN,
        predictedWinner VARCHAR(255),
        predictedWinner2 VARCHAR(255),
        predictedWinner3 VARCHAR(255),
        predictedWinner4 VARCHAR(255),
        predictedWinner5 VARCHAR(255),
        earlyWinner VARCHAR(255),
        theWinner VARCHAR(255),
        featuredWinner VARCHAR(255),
        correct BOOLEAN
    )
""")

conn.commit()

# Insert data into the table
cursor.execute("TRUNCATE TABLE games;")

cursor.executemany("""
    INSERT INTO games (gameId, awayTeamId, homeTeamId, awayTeamName, homeTeamName, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, isWinnerAway, isWinnerHome)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", records)

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()