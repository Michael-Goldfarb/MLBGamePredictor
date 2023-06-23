import requests
import json
import psycopg2
from datetime import datetime

# ONLY RETURN PREDICTION OF WHO IS GOING TO WIN IF GAME HASN'T STARTED


# first table with game information

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
    # if it has ended, get a "isWinner" field to see who wins
    isWinnerAway = game['teams']['away'].get('isWinner')
    isWinnerHome = game['teams']['home'].get('isWinner')
    records.append((gameId, link, awayTeamId, awayTeamId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome))

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
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

    # ONLY RETURN ODDS IF GAME HASN'T STARTED

conn.commit()

# Insert data into the table
cursor.execute("TRUNCATE TABLE games, LineupAndProbables, pitchingStats, hittingStats;")

cursor.executemany("""
    INSERT INTO games (gameId, link, awayTeamId, homeTeamId, awayTeamName, homeTeamName, gameStatus, gameDate, gameTime, awayTeamScore, homeTeamScore, awayTeamWinPct, homeTeamWinPct, venue, isWinnerAway, isWinnerHome)
    VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", records)























# Create the "LineupAndProbables" table (if it doesn't exist)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS LineupAndProbables (
        awayId INTEGER,
        awayName TEXT,
        homeId INTEGER,
        homeName TEXT,
        batterOneAway INTEGER,
        batterTwoAway INTEGER,
        batterThreeAway INTEGER,
        batterFourAway INTEGER,
        batterFiveAway INTEGER,
        batterSixAway INTEGER,
        batterSevenAway INTEGER,
        batterEightAway INTEGER,
        batterNineAway INTEGER,
        batterOneHome INTEGER,
        batterTwoHome INTEGER,
        batterThreeHome INTEGER,
        batterFourHome INTEGER,
        batterFiveHome INTEGER,
        batterSixHome INTEGER,
        batterSevenHome INTEGER,
        batterEightHome INTEGER,
        batterNineHome INTEGER,
        pitcherIdHome TEXT,
        pitcherIdAway TEXT,
        pitcherNameHome TEXT,
        pitcherNameAway TEXT
    );
""")  

unique_games = []
game_ids = set()

# Loop through each gameId and create rows in the "LineupAndProbables" table
for game in games:
    gameId = game['gamePk']
    if gameId not in game_ids:
        unique_games.append(game)
        game_ids.add(gameId)
for game in unique_games:
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game['gamePk']}/feed/live"
    response = requests.get(url)
    data = response.json()

    awayTeam = data['gameData']['teams']['away']
    homeTeam = data['gameData']['teams']['home']

    # Parse battingOrder if it is a string representation of an array
    battingOrderHome_str = data['liveData']['boxscore']['teams']['home'].get('battingOrder')
    if isinstance(battingOrderHome_str, str):
        battingOrderHome = json.loads(battingOrderHome_str)
    else:
        battingOrderHome = battingOrderHome_str

    battingOrderAway_str = data['liveData']['boxscore']['teams']['away'].get('battingOrder')
    if isinstance(battingOrderAway_str, str):
        battingOrderAway = json.loads(battingOrderAway_str)
    else:
        battingOrderAway = battingOrderAway_str

    probablePitcherHome = data['gameData']['probablePitchers']['home']
    probablePitcherAway = data['gameData']['probablePitchers']['away']



    # Check if battingOrderAway has at least 9 elements
    if len(battingOrderAway) >= 9:
        batterOneAway = battingOrderAway[0]
        batterTwoAway = battingOrderAway[1]
        batterThreeAway = battingOrderAway[2]
        batterFourAway = battingOrderAway[3]
        batterFiveAway = battingOrderAway[4]
        batterSixAway = battingOrderAway[5]
        batterSevenAway = battingOrderAway[6]
        batterEightAway = battingOrderAway[7]
        batterNineAway = battingOrderAway[8]
    else:
        # Set default values or handle the case where there are not enough elements
        batterOneAway = None
        batterTwoAway = None
        batterThreeAway = None
        batterFourAway = None
        batterFiveAway = None
        batterSixAway = None
        batterSevenAway = None
        batterEightAway = None
        batterNineAway = None

    # Check if battingOrderHome has at least 9 elements
    if len(battingOrderHome) >= 9:
        batterOneHome = battingOrderHome[0]
        batterTwoHome = battingOrderHome[1]
        batterThreeHome = battingOrderHome[2]
        batterFourHome = battingOrderHome[3]
        batterFiveHome = battingOrderHome[4]
        batterSixHome = battingOrderHome[5]
        batterSevenHome = battingOrderHome[6]
        batterEightHome = battingOrderHome[7]
        batterNineHome = battingOrderHome[8]
    else:
        # Set default values or handle the case where there are not enough elements
        batterOneHome = None
        batterTwoHome = None
        batterThreeHome = None
        batterFourHome = None
        batterFiveHome = None
        batterSixHome = None
        batterSevenHome = None
        batterEightHome = None
        batterNineHome = None

    # Insert the data into the "LineupAndProbables" table
    cursor.execute("""
        INSERT INTO LineupAndProbables (
        awayId, awayName, homeId, homeName, batterOneAway, batterTwoAway, batterThreeAway, batterFourAway, batterFiveAway,
        batterSixAway, batterSevenAway, batterEightAway, batterNineAway, batterOneHome, batterTwoHome, batterThreeHome, batterFourHome, 
        batterFiveHome, batterSixHome, batterSevenHome, batterEightHome, batterNineHome, pitcherIdHome, pitcherIdAway, pitcherNameHome, 
        pitcherNameAway
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """,
    (
        awayTeam['id'], awayTeam['name'], homeTeam['id'], homeTeam['name'], batterOneAway, batterTwoAway, batterThreeAway, batterFourAway,
        batterFiveAway, batterSixAway, batterSevenAway, batterEightAway, batterNineAway, batterOneHome, batterTwoHome, batterThreeHome,
        batterFourHome, batterFiveHome, batterSixHome, batterSevenHome, batterEightHome, batterNineHome,
        probablePitcherHome['id'], probablePitcherAway['id'], probablePitcherHome['fullName'], probablePitcherAway['fullName']
    ))













# Create the hittingStats table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS HittingStats (
        teamId INTEGER,
        runs INTEGER,
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPlayed INTEGER,
        leftOnBase INTEGER,
        stolenBases INTEGER
    )
""")

# Get the hitting stats for the away team
for game in games:
    awayTeamId = game['teams']['away']['team']['id']
    homeTeamId = game['teams']['home']['team']['id']
    awayTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{awayTeamId}/stats?season=2023&group=hitting&stats=season"
    awayTeamStatsResponse = requests.get(awayTeamStatsUrl)
    awayTeamStatsData = awayTeamStatsResponse.json()
    awayTeamStats = awayTeamStatsData['stats'][0]['splits'][0]['stat']

    # Insert data into the hittingStats table
    cursor.execute("""
        INSERT INTO hittingStats (
            teamId, runs, obp, slg, ops, gamesPlayed, leftOnBase, stolenBases
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        awayTeamId, awayTeamStats['runs'], awayTeamStats['obp'], awayTeamStats['slg'],
        awayTeamStats['ops'], awayTeamStats['gamesPlayed'], awayTeamStats['leftOnBase'],
        awayTeamStats['stolenBases']
    ))

    # Get the hitting stats for the home team
    homeTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{homeTeamId}/stats?season=2023&group=hitting&stats=season"
    homeTeamStatsResponse = requests.get(homeTeamStatsUrl)
    homeTeamStatsData = homeTeamStatsResponse.json()
    homeTeamStats = homeTeamStatsData['stats'][0]['splits'][0]['stat']

    # Insert data into the hittingStats table
    cursor.execute("""
        INSERT INTO hittingStats (
            teamId, runs, obp, slg, ops, gamesPlayed, leftOnBase, stolenBases
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        homeTeamId, homeTeamStats['runs'], homeTeamStats['obp'], homeTeamStats['slg'],
        homeTeamStats['ops'], homeTeamStats['gamesPlayed'], homeTeamStats['leftOnBase'],
        homeTeamStats['stolenBases']
    ))












# Create the PitchingStats table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PitchingStats (
        teamId INTEGER,
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

# Loop through each game and get the pitching statistics
for game in games:
    awayTeamId = game['teams']['away']['team']['id']
    homeTeamId = game['teams']['home']['team']['id']
    awayTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{awayTeamId}/stats?season=2023&group=pitching&stats=season"
    homeTeamStatsUrl = f"https://statsapi.mlb.com/api/v1/teams/{homeTeamId}/stats?season=2023&group=pitching&stats=season"

    # Get the pitching statistics for the away team
    awayTeamStatsResponse = requests.get(awayTeamStatsUrl)
    awayTeamStatsData = awayTeamStatsResponse.json()
    awayTeamStats = awayTeamStatsData['stats'][0]['splits'][0]['stat']

    # Insert data into the PitchingStats table for the away team
    cursor.execute("""
        INSERT INTO PitchingStats (
            teamId, era, whip, hitsPer9Inn, runsScoredPer9, homeRunsPer9, obp, slg, ops, gamesPitched,
            strikeOuts, saves, blownSaves, strikeoutWalkRatio
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        awayTeamId, awayTeamStats['era'], awayTeamStats['whip'], awayTeamStats['hitsPer9Inn'],
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
            teamId, era, whip, hitsPer9Inn, runsScoredPer9, homeRunsPer9, obp, slg, ops, gamesPitched,
            strikeOuts, saves, blownSaves, strikeoutWalkRatio
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        homeTeamId, homeTeamStats['era'], homeTeamStats['whip'], homeTeamStats['hitsPer9Inn'],
        homeTeamStats['runsScoredPer9'], homeTeamStats['homeRunsPer9'], homeTeamStats['obp'],
        homeTeamStats['slg'], homeTeamStats['ops'], homeTeamStats['gamesPitched'], homeTeamStats['strikeOuts'],
        homeTeamStats['saves'], homeTeamStats['blownSaves'], homeTeamStats['strikeoutWalkRatio']
    ))











    # TODO - Create a table that shows individual stats - such as the starting pitchers stats, the individual batters in the lineup stats, etc.
    # so for every player in game - return their hitting stats
    # get hitting stats from https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2023&group=hitting&startDate=03/30/2023&endDate={currentDate}&leagueListId=mlb_milb
    currentDate = datetime.now().strftime("%m/%d/%Y")





# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
