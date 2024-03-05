import requests
import json
import psycopg2
import os
from datetime import datetime

# response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-07-22&endDate=2023-07-22")
response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()
games = data['dates'][0]['games']

records = []
for game in games:
    gameId = game['gamePk']
    link = game['link']
    awayTeamId = game['teams']['away']['team']['id']
    homeTeamId = game['teams']['home']['team']['id']
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

    # Append record for the away team
    records.append((gameId, link, awayTeamId, awayTeamName, gameStatus, gameDate, gameTime, awayTeamScore, awayTeamWinPct, venue, isWinnerAway, None, None, None, None, None))

    # Append record for the home team
    records.append((gameId, link, homeTeamId, homeTeamName, gameStatus, gameDate, gameTime, homeTeamScore, homeTeamWinPct, venue, isWinnerHome, None, None, None, None, None))

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
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gamesv3 (
        gameId TEXT,
        link VARCHAR(255),
        teamId INTEGER,
        teamName VARCHAR(255),
        gameStatus VARCHAR(255),
        gameDate DATE,
        gameTime TIME,
        teamScore INTEGER,
        teamWinPct FLOAT,
        venue VARCHAR(255),
        isWinner BOOLEAN,
        predictedWinner VARCHAR(255),
        predictedWinner2 VARCHAR(255),
        predictedWinner3 VARCHAR(255),
        predictedWinner4 VARCHAR(255),
        predictedWinner5 VARCHAR(255)
    )
""")

conn.commit()

# Insert data into the table
cursor.execute("TRUNCATE TABLE gamesv3;")

cursor.executemany("""
    INSERT INTO gamesv3 (gameId, link, teamId, teamName, gameStatus, gameDate, gameTime, teamScore, teamWinPct, venue, isWinner, predictedWinner, predictedWinner2, predictedWinner3, predictedWinner4, predictedWinner5)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", records)

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
