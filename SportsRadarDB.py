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
apiKey = "eetqgrmb2hd7qcn3by9rv638"
url = f"https://api.sportradar.com/mlb/trial/v7/en/games/{todaysDate}/schedule.json?api_key={apiKey}"
response = requests.get(url)
data = response.json()
games = data["games"]

# Create the games2 table
create_games_table_query = """
CREATE TABLE IF NOT EXISTS games2 (
    id SERIAL PRIMARY KEY,
    gameId TEXT,
    status TEXT,
    game_time TIME,
    game_date DATE,
    venue_name TEXT,
    venue_id TEXT,
    home_team_name TEXT,
    home_team_market TEXT,
    home_team_id TEXT,
    away_team_name TEXT,
    away_team_market TEXT,
    away_team_id TEXT
)
"""
cursor.execute(create_games_table_query)


# Create the awayTeamStats table
create_stats_table_query = """
CREATE TABLE IF NOT EXISTS awayTeamStats (
    id SERIAL PRIMARY KEY,
    ops FLOAT,
    obp FLOAT,
    slg FLOAT,
    team_lob INTEGER,
    ab_risp INTEGER,
    era_overall FLOAT,
    whip_overall FLOAT,
    k9_overall FLOAT,
    babip_overall FLOAT,
    save INTEGER,
    blown_save INTEGER,
    era_bullpen FLOAT,
    whip_bullpen FLOAT,
    k9_bullpen FLOAT,
    babip_bullpen FLOAT,
    fpct FLOAT
)
"""
cursor.execute(create_stats_table_query)

awayTeamIds = []
homeTeamIds = []
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
    homeTeamIds.append(homeTeamId)
    awayTeamName = game["away"]["name"]
    awayTeamMarket = game["away"]["market"]
    awayTeamId = game["away"]["id"]
    awayTeamIds.append(awayTeamId)
    records.append((gameId, status, gameTime, gameDate, venueName, venueId, homeTeamName, homeTeamMarket, homeTeamId, awayTeamName, awayTeamMarket, awayTeamId))

    # Insert data into the games2 table
    insert_query = """
    INSERT INTO games2 (
        gameId,
        status,
        game_time,
        game_date,
        venue_name,
        venue_id,
        home_team_name,
        home_team_market,
        home_team_id,
        away_team_name,
        away_team_market,
        away_team_id
    ) VALUES (%s, %s, %s::time, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (gameId, status, gameTime, gameDate, venueName, venueId, homeTeamName, homeTeamMarket, homeTeamId, awayTeamName, awayTeamMarket, awayTeamId))

# Fetch away team stats
for team in awayTeamIds:
    secondUrl = f"https://api.sportradar.com/mlb/trial/v7/en/seasons/2023/reg/teams/{team}/statistics.json?api_key={apiKey}"
    away_team_stats_url = secondUrl
    print(secondUrl)
    away_team_stats_response = requests.get(away_team_stats_url)
    print(away_team_stats_response.text)
    print("hell yeah")
    try:
        away_team_stats_data = json.loads(away_team_stats_response.text)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        continue
    hitting_stats = away_team_stats_data["statistics"]["hitting"]["overall"]
    pitching_overall_stats = away_team_stats_data["statistics"]["pitching"]["overall"]
    pitching_bullpen_stats = away_team_stats_data["statistics"]["pitching"]["bullpen"]
    fielding_stats = away_team_stats_data["statistics"]["fielding"]["overall"]
    
    # Extract the desired stats
    ops = hitting_stats["ops"]
    obp = hitting_stats["obp"]
    slg = hitting_stats["slg"]
    team_lob = hitting_stats["team_lob"]
    ab_risp = hitting_stats["ab_risp"]
    
    era_overall = pitching_overall_stats["era"]
    whip_overall = pitching_overall_stats["whip"]
    k9_overall = pitching_overall_stats["k9"]
    babip_overall = pitching_overall_stats["babip"]
    save = pitching_overall_stats["games"]["save"]
    blown_save = pitching_overall_stats["games"]["blown_save"]
    
    era_bullpen = pitching_bullpen_stats["era"]
    whip_bullpen = pitching_bullpen_stats["whip"]
    k9_bullpen = pitching_bullpen_stats["k9"]
    babip_bullpen = pitching_bullpen_stats["babip"]
    
    fpct = fielding_stats["fpct"]

    # Insert data into the awayTeamStats table
cursor.execute(
    "INSERT INTO away_team_data (ops, obp, slg, team_lob, ab_risp, "
    "era_overall, whip_overall, k9_overall, babip_overall, "
    "save, blown_save, era_bullpen, "
    "whip_bullpen, k9_bullpen, babip_bullpen, fpct) "
    "VALUES (%s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (
        ops, obp, slg, team_lob, ab_risp,
        era_overall, whip_overall, k9_overall, babip_overall,
        save, blown_save, era_bullpen,
        whip_bullpen, k9_bullpen, babip_bullpen, fpct
    )
)
# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
