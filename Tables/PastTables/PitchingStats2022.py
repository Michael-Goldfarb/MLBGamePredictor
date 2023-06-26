import requests
import json
import psycopg2
from datetime import datetime

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-06-07&endDate=2022-08-07")
data = response.json()

conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PitchingStats2022 (
        teamId INTEGER,
        gameDate DATE,
        teamName VARCHAR(255),
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
        strikeoutWalkRatio VARCHAR(255),
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
        if i == 0: # uses the first game twice for some reason
            i += 1
            continue
        awayTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{awayTeamId}/stats?stats=byDateRange&season=2022&group=pitching&startDate=04/07/2022&endDate={gameDate}&leagueListId=mlb"
        awayTeamStatsResponse = requests.get(awayTeamStatsUrl)
        awayTeamStatsData = awayTeamStatsResponse.json()
        awayTeamStats = awayTeamStatsData['stats'][0]['splits'][0]['stat']

        # Insert data into the PitchingStats2022 table for the away team
        cursor.execute("""
            INSERT INTO PitchingStats2022 (
                teamId, gameDate, teamName, era, whip, hitsPer9Inn, runsScoredPer9, homeRunsPer9, obp, slg, ops, gamesPitched,
                strikeOuts, saves, blownSaves, strikeoutWalkRatio, isWinner
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            awayTeamId, gameDate, awayTeamName, awayTeamStats['era'], awayTeamStats['whip'], awayTeamStats['hitsPer9Inn'],
            awayTeamStats['runsScoredPer9'], awayTeamStats['homeRunsPer9'], awayTeamStats['obp'], awayTeamStats['slg'],
            awayTeamStats['ops'], awayTeamStats['gamesPitched'], awayTeamStats['strikeOuts'], awayTeamStats['saves'],
            awayTeamStats['blownSaves'], awayTeamStats['strikeoutWalkRatio'], isWinnerAway
        ))

        homeTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{homeTeamId}/stats?stats=byDateRange&season=2022&group=pitching&startDate=04/07/2022&endDate={gameDate}&leagueListId=mlb"
        homeTeamStatsResponse = requests.get(homeTeamStatsUrl)
        homeTeamStatsData = homeTeamStatsResponse.json()
        homeTeamStats = homeTeamStatsData['stats'][0]['splits'][0]['stat']
        
        # Insert data into the PitchingStats2022 table for the home team
        cursor.execute("""
            INSERT INTO PitchingStats2022 (
                teamId, gameDate, teamName, era, whip, hitsPer9Inn, runsScoredPer9, homeRunsPer9, obp, slg, ops, gamesPitched,
                strikeOuts, saves, blownSaves, strikeoutWalkRatio, isWinner
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            homeTeamId, gameDate, homeTeamName, homeTeamStats['era'], homeTeamStats['whip'], homeTeamStats['hitsPer9Inn'],
            homeTeamStats['runsScoredPer9'], homeTeamStats['homeRunsPer9'], homeTeamStats['obp'], homeTeamStats['slg'],
            homeTeamStats['ops'], homeTeamStats['gamesPitched'], homeTeamStats['strikeOuts'], homeTeamStats['saves'],
            homeTeamStats['blownSaves'], homeTeamStats['strikeoutWalkRatio'], isWinnerHome
        ))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()