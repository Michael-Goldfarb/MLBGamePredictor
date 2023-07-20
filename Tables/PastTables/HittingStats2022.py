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
    CREATE TABLE IF NOT EXISTS HittingStats2022v3 (
        teamId INTEGER,
        gameId VARCHAR(255),
        gameDate DATE,
        teamName VARCHAR(255),
        runs INTEGER,
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPlayed INTEGER,
        leftOnBase INTEGER,
        stolenBases INTEGER,
        isWinner BOOLEAN
    )
""")
i = 0;               
for date_info in data["dates"]:
    for game in date_info["games"]:
        gameId = game['gamePk']
        gameDate = game['officialDate']
        print(gameDate)
        awayTeamId = game['teams']['away']['team']['id']
        homeTeamId = game['teams']['home']['team']['id']
        awayTeamName = game['teams']['away']['team']['name']
        homeTeamName = game['teams']['home']['team']['name']
        isWinnerAway = game['teams']['away'].get('isWinner')
        isWinnerHome = game['teams']['home'].get('isWinner')
        if gameId == 663466: # all star game
            continue
        # if i == 0: # uses the first game twice for some reason
        #     i += 1
        #     continue

        awayTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{awayTeamId}/stats?stats=byDateRange&season=2022&group=hitting&startDate=04/07/2022&endDate={gameDate}&leagueListId=mlb"
        awayTeamStatsResponse = requests.get(awayTeamStatsUrl)
        awayTeamStatsData = awayTeamStatsResponse.json()
        awayTeamStats = awayTeamStatsData['stats'][0]['splits'][0]['stat']
        print(gameId)

        # Insert data into the HittingStats2022 table for the away team
        cursor.execute("""
            INSERT INTO HittingStats2022v3 (
                teamId, gameId, gameDate, teamName, runs, obp, slg, ops, gamesPlayed, leftOnBase, stolenBases, isWinner
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            awayTeamId, gameId, gameDate, awayTeamName, awayTeamStats['runs'], awayTeamStats['obp'], awayTeamStats['slg'],
            awayTeamStats['ops'], awayTeamStats['gamesPlayed'], awayTeamStats['leftOnBase'],
            awayTeamStats['stolenBases'], isWinnerAway
        ))

        homeTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{homeTeamId}/stats?stats=byDateRange&season=2022&group=hitting&startDate=04/07/2022&endDate={gameDate}&leagueListId=mlb"
        homeTeamStatsResponse = requests.get(homeTeamStatsUrl)
        homeTeamStatsData = homeTeamStatsResponse.json()
        homeTeamStats = homeTeamStatsData['stats'][0]['splits'][0]['stat']

        # Insert data into the HittingStats2022 table for the home team
        cursor.execute("""
        INSERT INTO HittingStats2022v3 (
                teamId, gameId, gameDate, teamName, runs, obp, slg, ops, gamesPlayed, leftOnBase, stolenBases, isWinner
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            homeTeamId, gameId, gameDate, homeTeamName, homeTeamStats['runs'], homeTeamStats['obp'], homeTeamStats['slg'],
            homeTeamStats['ops'], homeTeamStats['gamesPlayed'], homeTeamStats['leftOnBase'],
            homeTeamStats['stolenBases'], isWinnerHome
        ))

        print("DONE")

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()