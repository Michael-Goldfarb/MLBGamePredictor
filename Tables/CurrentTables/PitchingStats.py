import requests
import json
import psycopg2
from datetime import datetime

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
# response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-07-18&endDate=2023-07-18")
data = response.json()
games = data['dates'][0]['games']

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
# Create the PitchingStats table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PitchingStats (
        teamId INTEGER,
        gameId TEXT,
        team_name VARCHAR(255),
        era VARCHAR(255),
        whip VARCHAR(255),
        hitsPer9Inn VARCHAR(255),
        runsScoredPer9 VARCHAR(255),
        homeRunsPer9 VARCHAR(255),
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPitched INTEGER,
        strikeOuts INTEGER,
        saves INTEGER,
        blownSaves INTEGER,
        strikeoutWalkRatio VARCHAR(255)
    )
""")
               
# Truncate the table before inserting new data
cursor.execute("TRUNCATE TABLE PitchingStats;")

# Loop through each game and get the pitching statistics
for game in games:
    gameId = game['gamePk']
    awayTeamId = game['teams']['away']['team']['id']
    homeTeamId = game['teams']['home']['team']['id']
    awayTeamName = game['teams']['away']['team']['name']
    homeTeamName = game['teams']['home']['team']['name']
    awayTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{awayTeamId}/stats?season=2023&group=pitching&stats=season"
    homeTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{homeTeamId}/stats?season=2023&group=pitching&stats=season"

    # Get the pitching statistics for the away team
    awayTeamStatsResponse = requests.get(awayTeamStatsUrl)
    awayTeamStatsData = awayTeamStatsResponse.json()
    awayTeamStats = awayTeamStatsData['stats'][0]['splits'][0]['stat']

    # Insert data into the PitchingStats table for the away team
    cursor.execute("""
        INSERT INTO PitchingStats (
            teamId, gameId, team_name, era, whip, hitsPer9Inn, runsScoredPer9, homeRunsPer9, obp, slg, ops, gamesPitched,
            strikeOuts, saves, blownSaves, strikeoutWalkRatio
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        awayTeamId, gameId, awayTeamName, awayTeamStats['era'], awayTeamStats['whip'], awayTeamStats['hitsPer9Inn'],
        awayTeamStats['runsScoredPer9'], awayTeamStats['homeRunsPer9'], awayTeamStats['obp'],
        awayTeamStats['slg'], awayTeamStats['ops'], awayTeamStats['gamesPitched'], awayTeamStats['strikeOuts'],
        awayTeamStats['saves'], awayTeamStats['blownSaves'], awayTeamStats['strikeoutWalkRatio']
    ))

    # Get the pitching statistics for the home team
    homeTeamStatsResponse = requests.get(homeTeamStatsUrl)
    homeTeamStatsData = homeTeamStatsResponse.json()
    homeTeamStats = homeTeamStatsData['stats'][0]['splits'][0]['stat']

    # Insert data into the PitchingStats table for the home team
    cursor.execute("""
        INSERT INTO PitchingStats (
            teamId, gameId, team_name, era, whip, hitsPer9Inn, runsScoredPer9, homeRunsPer9, obp, slg, ops, gamesPitched,
            strikeOuts, saves, blownSaves, strikeoutWalkRatio
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        homeTeamId, gameId, homeTeamName, homeTeamStats['era'], homeTeamStats['whip'], homeTeamStats['hitsPer9Inn'],
        homeTeamStats['runsScoredPer9'], homeTeamStats['homeRunsPer9'], homeTeamStats['obp'],
        homeTeamStats['slg'], homeTeamStats['ops'], homeTeamStats['gamesPitched'], homeTeamStats['strikeOuts'],
        homeTeamStats['saves'], homeTeamStats['blownSaves'], homeTeamStats['strikeoutWalkRatio']
    ))


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()