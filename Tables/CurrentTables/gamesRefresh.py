import requests
import json
import psycopg2
from datetime import datetime
import pytz

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
        insertedYet VARCHAR(255)
    )
""")

# Initialize counters
numerator = 0
denominator = 0

# Get the current date
currentDate = games[0]['gameDate']
est_timezone = pytz.timezone('America/New_York')
gameDateEST = datetime.strptime(currentDate, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc).astimezone(est_timezone)
gameDateString = gameDateEST.strftime("%Y-%m-%d %H:%M:%S %Z")

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

    # Retrieve the value of teamName, numerator, denominator, and insertedYet from the teamRecords table for the specific gameId
    cursor.execute("SELECT numerator, denominator, insertedYet FROM teamRecords WHERE teamName ILIKE %s;", (awayTeamName,))
    row = cursor.fetchone()
    updateAway = 0
    if row is not None:
        numeratorAway = row[0]
        denominatorAway = row[1]
        insertedYet = row[2]
    else:
        numeratorAway = 0
        denominatorAway = 0
        insertedYet = ""
        updateAway+=1
        print("New info")
    
    if gameStatus != "Final" and gameStatus != "Postponed" and gameStatus != "Suspended":
        insertedYetAway = "No" + gameDateString + str(gameId)
    else:
        insertedYetAway = "Yes" + gameDateString + str(gameId)
    if insertedYet == insertedYetAway and insertedYetAway[:3] == "Yes":
        alreadyStoredAway = True
    else:
        alreadyStoredAway = False
   
    # Retrieve the value of teamName, numerator, denominator, and insertedYet from the teamRecords table for the specific gameId
    cursor.execute("SELECT numerator, denominator, insertedYet FROM teamRecords WHERE teamName ILIKE %s;", (homeTeamName,))
    row = cursor.fetchone()
    updateHome = 0
    if row is not None:
        numeratorHome = row[0]
        denominatorHome = row[1]
        insertedYet = row[2]
    else:
        numeratorHome = 0
        denominatorHome = 0
        insertedYet = ""
        updateHome+=1
        print("New info")
    
    if gameStatus != "Final" and gameStatus != "Postponed" and gameStatus != "Suspended":
        insertedYetHome = "No" + gameDateString + str(gameId)
    else:
        insertedYetHome = "Yes" + gameDateString + str(gameId)
    if insertedYet == insertedYetHome and insertedYetAway[:3] == "Yes":
        alreadyStoredHome = True
    else:
        alreadyStoredHome = False
   

    # Determine the correct value based on the conditions
    starter = 0
    updatedOrNo = False
    if isWinnerAway and awayTeamName == theWinner:
        correct = True
        starter+=1
        numerator += 1
        denominator += 1
        numeratorAway += 1
        numeratorHome += 1
        denominatorAway += 1
        denominatorHome += 1
        updatedOrNo = True
    elif isWinnerHome and homeTeamName == theWinner:
        correct = True
        starter+=1
        numerator += 1
        denominator += 1
        numeratorHome += 1
        numeratorAway += 1
        denominatorAway += 1
        denominatorHome += 1
        updatedOrNo = True
    elif isWinnerAway is None or isWinnerHome is None:
        correct = None
    else:
        if gameStatus != "Postponed" and gameStatus != "Suspended" and theWinner != None:
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
            INSERT INTO teamRecords (teamName, numerator, denominator, percentage, insertedYet)
            VALUES (%s, %s, %s, %s, %s)
        """, (awayTeamName, numeratorAway, denominatorAway, percentages, insertedYetAway))
    else:
        if gameStatus == "Final" and alreadyStoredAway == False and correct != None:
            if denominatorAway > 0:
                percentages = float(numeratorAway)/denominatorAway
            else:
                percentages = 0.0
            cursor.execute("""
                UPDATE teamRecords
                SET numerator = %s, denominator = %s, percentage = %s, insertedYet = %s
                WHERE teamName = %s
            """, (numeratorAway, denominatorAway, percentages, insertedYetAway, awayTeamName))
    if updateHome == 1:
        if denominatorHome != 0:
            percentages = float(numeratorHome)/denominatorHome
        else:
            percentages = None
        cursor.execute("""
            INSERT INTO teamRecords (teamName, numerator, denominator, percentage, insertedYet)
            VALUES (%s, %s, %s, %s, %s)
        """, (homeTeamName, numeratorHome, denominatorHome, percentages, insertedYetHome))
    else:
        if gameStatus == "Final" and alreadyStoredHome == False and correct != None:
            if denominatorHome > 0:
                percentages = float(numeratorHome)/denominatorHome
            else:
                percentages = 0.0
            cursor.execute("""
                UPDATE teamRecords
                SET numerator = %s, denominator = %s, percentage = %s, insertedYet = %s
                WHERE teamName = %s
            """, (numeratorHome, denominatorHome, percentages, insertedYetHome, homeTeamName))
    records.append((gameId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome, correct))

# Calculate the fraction of correct predictions
if denominator > 0:
    fraction_numerator = numerator
    fraction_denominator = denominator
else:
    fraction_numerator = None
    fraction_denominator = None

# Insert the daily prediction into the dailyPredictions table
cursor.execute("""
    INSERT INTO dailyPredictions (prediction_date, numerator, denominator)
    VALUES (%s, %s, %s)
    ON CONFLICT (prediction_date) DO UPDATE
    SET numerator = EXCLUDED.numerator, denominator = EXCLUDED.denominator
""", (gameDateEST, fraction_numerator, fraction_denominator))



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
