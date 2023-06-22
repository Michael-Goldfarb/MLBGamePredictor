import requests
import json
import psycopg2

# Step 1: Retrieve the data
response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
data = response.json()

# Step 2: Parse the JSON
games = data['dates'][0]['games']

# Step 3: Extract the required fields
records = []
for game in games:
    game_id = game['gamePk']
    team1 = game['teams']['away']['team']['name']
    team2 = game['teams']['home']['team']['name']
    game_date = game['gameDate']
    start_time_tbd = game['status']['startTimeTBD']
    venue = game['venue']['name']
    records.append((game_id, team1, team2, game_date, start_time_tbd, venue))

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
        id INT,
        team1 VARCHAR(255),
        team2 VARCHAR(255),
        gameDate DATE,
        startTimeTBD BOOLEAN,
        venue VARCHAR(255),
        PRIMARY KEY (id)
    )
""")

conn.commit()

# Step 6: Insert data into the table
cursor.executemany("""
    INSERT INTO games (id, team1, team2, gameDate, startTimeTBD, venue)
    VALUES (%s, %s, %s, %s, %s, %s)
""", records)
conn.commit()

# Close the connection
cursor.close()
conn.close()
