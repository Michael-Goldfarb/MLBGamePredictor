import requests
import json
import psycopg2
from datetime import datetime
import os

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-04-20&endDate=2022-10-01")
data = response.json()

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
    CREATE TABLE IF NOT EXISTS games2022 (
        gameId SERIAL PRIMARY KEY,
        link VARCHAR(255),
        awayTeamId INTEGER,
        homeTeamId INTEGER,
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
        isWinnerHome BOOLEAN
    )
""")
               
records = []
i = 0
for date_info in data["dates"]:
    for game in date_info["games"]:
        gameId = game['gamePk']
        link = game['link']
        awayTeamId = game['teams']['away']['team']['id']
        homeTeamId = game['teams']['home']['team']['id']
        awayTeamName = game['teams']['away']['team']['name']
        homeTeamName = game['teams']['home']['team']['name']
        gameStatus = game["status"]["detailedState"]
        gameDate = game['gameDate']
        print(gameDate)
        gameTime = game['gameDate'][11:16]
        awayTeamScore = game['teams']['away'].get('score')
        homeTeamScore = game['teams']['home'].get('score')
        awayTeamWinPct = game["teams"]["away"]["leagueRecord"]["pct"]
        homeTeamWinPct = game["teams"]["home"]["leagueRecord"]["pct"]
        venue = game['venue']['name']
        isWinnerAway = game['teams']['away'].get('isWinner')
        isWinnerHome = game['teams']['home'].get('isWinner')
        if i == 0: # uses the first game twice for some reason
            i += 1
            continue
        if gameId == 663466: # all star game
            continue
        records.append((gameId, link, awayTeamId, homeTeamId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome))

    # Insert data into the table
    cursor.execute("TRUNCATE TABLE games2022;")

    # Filter out duplicate records
    unique_records = []
    seen_game_ids = set()
    for record in records:
        gameId = record[0]
        if gameId not in seen_game_ids:
            unique_records.append(record)
            seen_game_ids.add(gameId)

    # Insert data into the table
    cursor.executemany("""
        INSERT INTO games2022 (gameId, link, awayTeamId, homeTeamId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, unique_records)

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()