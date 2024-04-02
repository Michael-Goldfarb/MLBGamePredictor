import requests
import json
import psycopg2
from datetime import datetime
import os

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
# response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2023-07-22&endDate=2023-07-22")
data = response.json()
games = data['dates'][0]['games']

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
# Create the hittingStats table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS HittingStats (
        gameId TEXT,
        teamId INTEGER,
        team_name VARCHAR(255),
        runs INTEGER,
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPlayed INTEGER,
        leftOnBase INTEGER,
        stolenBases INTEGER
    )
""")
               
# Truncate the table before inserting new data
cursor.execute("TRUNCATE TABLE hittingStats;")

# Get the hitting stats for the away team
for game in games:
    gameId = game['gamePk']
    awayTeamId = game['teams']['away']['team']['id']
    awayTeamName = game['teams']['away']['team']['name']
    homeTeamId = game['teams']['home']['team']['id']
    homeTeamName = game['teams']['home']['team']['name']
    awayTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{awayTeamId}/stats?season=2024&group=hitting&stats=season"
    print(awayTeamStatsUrl)
    # awayTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{awayTeamId}/stats?stats=byDateRange&group=hitting&startDate=2023-02-18&endDate=2023-07-22"
    awayTeamStatsResponse = requests.get(awayTeamStatsUrl)
    awayTeamStatsData = awayTeamStatsResponse.json()
    awayTeamStats = awayTeamStatsData['stats'][0]['splits'][0]['stat']

    # Insert data into the hittingStats table
    cursor.execute("""
        INSERT INTO hittingStats (
            gameId, teamId, team_name, runs, obp, slg, ops, gamesPlayed, leftOnBase, stolenBases
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        gameId, awayTeamId, awayTeamName, awayTeamStats['runs'], awayTeamStats['obp'], awayTeamStats['slg'],
        awayTeamStats['ops'], awayTeamStats['gamesPlayed'], awayTeamStats['leftOnBase'],
        awayTeamStats['stolenBases']
    ))

    # Get the hitting stats for the home team
    homeTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{homeTeamId}/stats?season=2024&group=hitting&stats=season"
    print(homeTeamStatsUrl)
    # homeTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{homeTeamId}/stats?stats=byDateRange&group=hitting&startDate=2023-02-18&endDate=2023-07-22"
    homeTeamStatsResponse = requests.get(homeTeamStatsUrl)
    homeTeamStatsData = homeTeamStatsResponse.json()
    homeTeamStats = homeTeamStatsData['stats'][0]['splits'][0]['stat']

    # Insert data into the hittingStats table
    cursor.execute("""
        INSERT INTO hittingStats (
            gameId, teamId, team_name, runs, obp, slg, ops, gamesPlayed, leftOnBase, stolenBases
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        gameId, homeTeamId, homeTeamName, homeTeamStats['runs'], homeTeamStats['obp'], homeTeamStats['slg'],
        homeTeamStats['ops'], homeTeamStats['gamesPlayed'], homeTeamStats['leftOnBase'],
        homeTeamStats['stolenBases']
    ))


# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()