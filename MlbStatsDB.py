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
starters = []
lineup = []
teamsLineup = []
teamsStarters = []

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
    probablePitcherHomeId = data['gameData']['probablePitchers']['home']['id']
    starters.append(probablePitcherHomeId)
    teamsStarters.append(homeTeamName)
    probablePitcherAway = data['gameData']['probablePitchers']['away']
    probablePitcherAwayId = data['gameData']['probablePitchers']['away']['id']
    starters.append(probablePitcherAwayId)
    teamsStarters.append(awayTeamName)

    awayTeamName = awayTeam['name']
    homeTeamName = homeTeam['name']

    # Check if battingOrderAway has at least 9 elements
    if len(battingOrderAway) >= 9:
        batterOneAway = battingOrderAway[0]
        lineup.append(battingOrderAway[0])
        teamsLineup.append(awayTeamName)
        batterTwoAway = battingOrderAway[1]
        lineup.append(battingOrderAway[1])
        teamsLineup.append(awayTeamName)
        batterThreeAway = battingOrderAway[2]
        lineup.append(battingOrderAway[2])
        teamsLineup.append(awayTeamName)
        batterFourAway = battingOrderAway[3]
        lineup.append(battingOrderAway[3])
        teamsLineup.append(awayTeamName)
        batterFiveAway = battingOrderAway[4]
        lineup.append(battingOrderAway[4])
        teamsLineup.append(awayTeamName)
        batterSixAway = battingOrderAway[5]
        lineup.append(battingOrderAway[5])
        teamsLineup.append(awayTeamName)
        batterSevenAway = battingOrderAway[6]
        lineup.append(battingOrderAway[6])
        teamsLineup.append(awayTeamName)
        batterEightAway = battingOrderAway[7]
        lineup.append(battingOrderAway[7])
        teamsLineup.append(awayTeamName)
        batterNineAway = battingOrderAway[8]
        lineup.append(battingOrderAway[8])
        teamsLineup.append(awayTeamName)
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
        lineup.append(battingOrderHome[0])
        teamsLineup.append(homeTeamName)
        batterTwoHome = battingOrderHome[1]
        lineup.append(battingOrderHome[1])
        teamsLineup.append(homeTeamName)
        batterThreeHome = battingOrderHome[2]
        lineup.append(battingOrderHome[2])
        teamsLineup.append(homeTeamName)
        batterFourHome = battingOrderHome[3]
        lineup.append(battingOrderHome[3])
        teamsLineup.append(homeTeamName)
        batterFiveHome = battingOrderHome[4]
        lineup.append(battingOrderHome[4])
        teamsLineup.append(homeTeamName)
        batterSixHome = battingOrderHome[5]
        lineup.append(battingOrderHome[5])
        teamsLineup.append(homeTeamName)
        batterSevenHome = battingOrderHome[6]
        lineup.append(battingOrderHome[6])
        teamsLineup.append(homeTeamName)
        batterEightHome = battingOrderHome[7]
        lineup.append(battingOrderHome[7])
        teamsLineup.append(homeTeamName)
        batterNineHome = battingOrderHome[8]
        lineup.append(battingOrderHome[8])
        teamsLineup.append(homeTeamName)
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

# Define the SQL statement to create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS lineupStats (
        player_id TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        team_name TEXT,
        games_played INTEGER,
        babip TEXT
    );
""")


# Loop through each player in the lineup
for index, player_id in enumerate(lineup):
    team_name = teamsLineup[index]  # Get the team name corresponding to the current player

    # Make the API request to fetch player stats
    api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2023&group=hitting&startDate=03/30/2023&endDate={currentDate}&leagueListId=mlb_milb".format(
        playerId=player_id,
        currentDate=datetime.now().strftime("%m/%d/%Y")
    )
    response = requests.get(api_url)
    data = response.json()

    # Extract the required fields
    stats = data["stats"][0]["splits"][0]["stat"]
    games_played = stats["gamesPlayed"]
    obp = stats["obp"]
    slg = stats["slg"]
    ops = stats["ops"]
    at_bats_per_home_run = stats["atBatsPerHomeRun"]
    babip = stats["babip"]

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO lineupStats (
            player_id, obp, slg, ops, at_bats_per_home_run, team_name, games_played, babip
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, obp, slg, ops, at_bats_per_home_run, team_name, games_played, babip
    ))































# TODO - Create a table that shows individual stats - such as the starting pitchers stats, the individual batters in the lineup stats, etc.
# so for every player in game - return their pitching stats
# get pitching stats from https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2023&group=pitching&startDate=03/30/2023&endDate={currentDate}&leagueListId=mlb_milb
currentDate = datetime.now().strftime("%m/%d/%Y")

# Define the SQL statement to create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS probablesStats (
        player_id TEXT,
        strikeoutWalkRatio TEXT,
        games_started INTEGER,
        hitsPer9Inn TEXT,
        strikeoutsPer9Inn TEXT,
        team_name TEXT,
        era TEXT,
        whip TEXT,
        walksPer9Inn TEXT
    );
""")


# Loop through each player in starters
for index, player_id in enumerate(starters):
    team_name = teamsStarters[index]  # Get the team name corresponding to the current player

    # Make the API request to fetch player stats
    api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2023&group=pitching&startDate=03/30/2023&endDate={currentDate}&leagueListId=mlb_milb".format(
        playerId=player_id,
        currentDate=datetime.now().strftime("%m/%d/%Y")  
    )
    response = requests.get(api_url)
    data = response.json()

    # Extract the required fields
    stats = data["stats"][0]["splits"][0]["stat"]
    strikeoutWalkRatio = stats["strikeoutWalkRatio"]
    games_started = stats["gamesStarted"]
    hitsPer9Inn = stats["hitsPer9Inn"]
    strikeoutsPer9Inn = stats["strikeoutsPer9Inn"]
    era = stats["era"]
    whip = stats["whip"]
    walksPer9Inn = stats["walksPer9Inn"]

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO probablesStats (
            player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
    ))





# MAKE ANOTHER TABLE WITH LAST YEARS STATS -- USE THIS TABLE IF GAMES_STARTED IS LESS THAN 5

cursor.execute("""
    CREATE TABLE IF NOT EXISTS previousYearPitchingStats (
        player_id TEXT,
        strikeoutWalkRatio TEXT,
        games_started INTEGER,
        hitsPer9Inn TEXT,
        strikeoutsPer9Inn TEXT,
        team_name TEXT,
        era TEXT,
        whip TEXT,
        walksPer9Inn TEXT
    );
""")
     # SEE IF THERE IS A DIFFERENCE IF IT IS A TEXT OR FLOAT

# Iterate over the starters
for index, playerId in enumerate(starters):
    team_name = teamsStarters[index]  # Get the team name corresponding to the current player
    url = f"https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2022&group=pitching&startDate=05/07/2022&endDate=10/05/2022&leagueListId=mlb_milb"
    response = requests.get(url)
    data = json.loads(response.text)
    player_id = playerId

    lastStatIndex = None  # Initialize lastStatIndex to None
    foundStat = False  # Flag to track if a satisfying element is found

    for idx, d in enumerate(data['stats']):
        if 'stat' in d:
            lastStatIndex = idx 
            foundStat = True
            break
    print(lastStatIndex)
    # Extract the required fields from the response
    if foundStat:
        stats = data['stats'][0][lastStatIndex]['stat']
        strikeoutWalkRatio = stats["strikeoutWalkRatio"]
        games_started = stats["gamesStarted"]
        hitsPer9Inn = stats["hitsPer9Inn"]
        strikeoutsPer9Inn = stats["strikeoutsPer9Inn"]
        era = stats["era"]
        whip = stats["whip"]
        walksPer9Inn = stats["walksPer9Inn"]
        pass
    else :
        stats = data["stats"][0]["splits"][0]["stat"]
        strikeoutWalkRatio = stats["strikeoutWalkRatio"]
        games_started = stats["gamesStarted"]
        hitsPer9Inn = stats["hitsPer9Inn"]
        strikeoutsPer9Inn = stats["strikeoutsPer9Inn"]
        era = stats["era"]
        whip = stats["whip"]
        walksPer9Inn = stats["walksPer9Inn"]
        pass

    # Insert the player stats into the table
    cursor.execute("""
        INSERT INTO previousYearPitchingStats (
            player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
        )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        player_id, strikeoutWalkRatio, games_started, hitsPer9Inn, strikeoutsPer9Inn, team_name, era, whip, walksPer9Inn
    ))




# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
