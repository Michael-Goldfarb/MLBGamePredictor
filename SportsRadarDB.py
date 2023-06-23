import requests
import json
import psycopg2
from datetime import datetime

# ONLY RETURN PREDICTION OF WHO IS GOING TO WIN IF GAME HASN'T STARTED

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
todaysDate = datetime.now().strftime("%Y/%m/%d")
current_date = datetime.now().strftime("%Y/%m/%d")
apiKey = "eetqgrmb2hd7qcn3by9rv638"
url = f"https://api.sportradar.com/mlb/trial/v7/en/games/{todaysDate}/schedule.json?api_key={apiKey}"
response = requests.get(url)
data = response.json()
games = data["games"]

records = []
for game in games:
    gameId = game["id"]
    status = game["status"]
    scheduled_datetime = datetime.strptime(game["scheduled"], "%Y-%m-%dT%H:%M:%S%z")
    gameTime = scheduled_datetime.strftime("%H:%M:%S")
    gameDate = data["date"]
    venueName = game["venue"]["name"]
    venueId = game["venue"]["id"]
    homeTeamName = game["home"]["name"]
    homeTeamMarket = game["home"]["market"]
    homeTeamId = game["home"]["id"]
    awayTeamName = game["away"]["name"]
    awayTeamMarket = game["away"]["market"]
    awayTeamId = game["away"]["id"]
    records.append((gameId, status, gameTime, gameDate, venueName, venueId, homeTeamName, homeTeamMarket, homeTeamId, awayTeamName, awayTeamMarket, awayTeamId))

cursor.execute("""
    CREATE TABLE IF NOT EXISTS games2 (
        id SERIAL PRIMARY KEY,
        gameId TEXT,
        status TEXT,
        gameTime TIME,
        gameDate DATE,
        venueName TEXT,
        venueId TEXT,
        homeTeamName TEXT,
        homeTeamMarket TEXT,
        homeTeamId TEXT,
        awayTeamName TEXT,
        awayTeamMarket TEXT,
        awayTeamId TEXT
    );
""")


# Insert data into the table
cursor.execute("TRUNCATE TABLE games2;")

# Insert the data into the "games" table
cursor.executemany("""
    INSERT INTO games2 (gameId, status, gameTime, gameDate, venueName, venueId, homeTeamName, homeTeamMarket, homeTeamId, awayTeamName, awayTeamMarket, awayTeamId) 
    VALUES (%s, %s, %s::time, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, records)


# Commit the changes to the database
conn.commit()











cursor.close()
conn.close()