import requests
import json
import psycopg2
from datetime import datetime

# response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-07-09&endDate=2023-07-09")
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
# cursor.execute("TRUNCATE TABLE gamesRefresh;")
               
# Create the teamRecords table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS teamRecords (
        teamName VARCHAR(255),
        numerator INTEGER,
        denominator INTEGER,
        percentage FLOAT,
        gameStatus VARCHAR(255)
    )
""")

# Initialize counters
numerator = 0
denominator = 0

records = []
for game in games:
    gameId = game['gamePk']
    awayTeamName = game['teams']['away']['team']['name']
    print(awayTeamName)
    homeTeamName = game['teams']['home']['team']['name']
    print(homeTeamName)
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

    # Retrieve the value of teamName, numerator, denominator, and gameStatus from the teamRecords table for the specific gameId
    cursor.execute("SELECT numerator, denominator, gameStatus FROM teamRecords WHERE teamName = CAST(%s AS text);", (awayTeamName,))
    row = cursor.fetchone()
    updateAway = 0
    if row is not None:
        numeratorAway = row[0]
        denominatorAway = row[1]
        gameStatus2 = row[2]
        if denominatorAway == 0:
            updateAway+=1
    else:
        numeratorAway = 0
        denominatorAway = 0
        updateAway+=1

    # Retrieve the value of teamName, numerator, denominator, and gameStatus from the teamRecords table for the specific gameId
    cursor.execute("SELECT numerator, denominator FROM teamRecords WHERE teamName = CAST(%s AS text);", (homeTeamName,))
    row = cursor.fetchone()
    updateHome = 0
    if row is not None:
        numeratorHome = row[0]
        denominatorHome = row[1]
        if denominatorHome == 0:
            updateHome+=1
    else:
        numeratorHome = 0
        denominatorHome = 0
        updateHome+=1
    
    # Determine the correct value based on the conditions
    starter = 0
    if isWinnerAway and awayTeamName == theWinner:
        print(awayTeamName)
        correct = True
        starter+=1
        numerator += 1
        denominator += 1
        numeratorAway += 1
        numeratorHome += 1
        denominatorAway += 1
        denominatorHome += 1
    elif isWinnerHome and homeTeamName == theWinner:
        print(homeTeamName)
        correct = True
        starter+=1
        numerator += 1
        denominator += 1
        numeratorHome += 1
        numeratorAway += 1
        denominatorAway += 1
        denominatorHome += 1
    elif isWinnerAway is None or isWinnerHome is None:
        correct = None
    else:
        correct = False
        starter+=1
        denominator += 1
        denominatorAway += 1
        denominatorHome += 1
    
    # Check the conditions before inserting into teamRecords
    if updateAway == 1:
        if denominatorAway != 0:
            percentages = float(numeratorAway)/denominatorAway
        else:
            percentages = None
        cursor.execute("""
            INSERT INTO teamRecords (teamName, numerator, denominator, percentage, gameStatus)
            VALUES (%s, %s, %s, %s, %s)
        """, (awayTeamName, numeratorAway, denominatorAway, percentages, gameStatus))
    else:
        if gameStatus == "Final" and gameStatus2 != "Final" and starter != 0:
            percentages = float(numeratorAway)/denominatorAway
            cursor.execute("""
                UPDATE teamRecords
                SET numerator = %s, denominator = %s, percentage = %s, gameStatus = %s
                WHERE teamName = %s
            """, (numeratorAway, denominatorAway, percentages, awayTeamName, gameStatus))
    if updateHome == 1:
        if denominatorHome != 0:
            percentages = float(numeratorAway)/denominatorAway
        else:
            percentages = None
        cursor.execute("""
            INSERT INTO teamRecords (teamName, numerator, denominator, percentage, gameStatus)
            VALUES (%s, %s, %s, %s, %s)
        """, (homeTeamName, numeratorHome, denominatorHome, percentages, gameStatus))
    else:
        if gameStatus == "Final" and gameStatus2 != "Final":
            percentages = float(numeratorAway)/denominatorAway
            cursor.execute("""
                UPDATE teamRecords
                SET numerator = %s, denominator = %s, percentage = %s, gameStatus = %s
                WHERE teamName = %s
            """, (numeratorHome, denominatorHome, percentages, homeTeamName, gameStatus))
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
cursor.executemany("""
    INSERT INTO gamesRefresh (gameId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome, correct)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", records)


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
