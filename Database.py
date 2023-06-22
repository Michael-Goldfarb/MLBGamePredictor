import requests
import json
import psycopg2

# ONLY RETURN ODDS IF GAME HASN'T STARTED


# Step 1: Retrieve the data
response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()

# Step 2: Parse the JSON
games = data['dates'][0]['games']

# Step 3: Extract the required fields
records = []
for game in games:
    gameId = game['gamePk']
    link = game['link']
    teamId1 = game['teams']['away']['team']['id']
    teamId2 = game['teams']['home']['team']['id']
    team1 = game['teams']['away']['team']['name']
    team2 = game['teams']['home']['team']['name']
    detailedState = game["status"]["detailedState"]
    gameDate = game['gameDate']
    gameTime = game['gameDate'][11:16]
    # get a "status" field, to show if the game has ended
    # if it has ended, get a "isWinner" field to see who wins
    #   is_winner = game.get("isWinner")  # Handles possible null value
    scoreTeam1 = game['teams']['home'].get('score', 0)
    scoreTeam2 = game['teams']['away'].get('score', 0)
    # FIX LEAGUE RECORD - IT RETURNS AN OBJECT, CHANGE IT TO RETURN THE PCT
    pctTeam1 = game["teams"]["away"]["leagueRecord"]["pct"]
    pctTeam2 = game["teams"]["home"]["leagueRecord"]["pct"]
    venue = game['venue']['name']
    records.append((gameId, link, teamId1, teamId2, team1, team2, detailedState, gameDate, gameTime, scoreTeam1, scoreTeam2, pctTeam1, pctTeam2, venue))

# Step 4: Set up a connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

# Step 5: Create a table
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        gameId SERIAL PRIMARY KEY,
        link VARCHAR(255),
        teamId1 INTEGER,
        teamId2 INTEGER,
        team1 VARCHAR(255),
        team2 VARCHAR(255),
        detailedState VARCHAR(255),
        gameDate DATE,
        gameTime TIME,
        scoreTeam1 INTEGER,
        scoreTeam2 INTEGER,
        pctTeam1 FLOAT,
        pctTeam2 FLOAT,
        venue VARCHAR(255)
    )
""")
               
    #ADD A SECTION FOR STARTING PITCHERS
    # GET THROUGH THIS LINK: https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live
    # THIS LINK IS EASIER FOR PROBABLES: https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher


    # ONLY RETURN ODDS IF GAME HASN'T STARTED

conn.commit()

# Step 6: Insert data into the table
cursor.executemany("""
    INSERT INTO games (gameId, link, teamId1, teamId2, team1, team2, detailedState, gameDate, gameTime, scoreTeam1, scoreTeam2, pctTeam1, pctTeam2, venue)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", records)
conn.commit()

# Close the connection
cursor.close()
conn.close()
