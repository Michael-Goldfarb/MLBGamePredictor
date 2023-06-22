host = 'your_host'
database = 'your_database'
user = 'your_username'
password = 'your_password'



conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)


cur = conn.cursor()


url = 'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1'
response = requests.get(url)
data = response.json()


games = data['dates'][0]['games']
for game in games:
    gamePk = game['gamePk']
    gameType = game['gameType']
    season = game['season']
    gameDate = game['gameDate']
    # Extract other relevant data fields as needed

    # Insert the data into the database
    cur.execute(

        # ASSUMES THAT THERE IS A TABLE CALLED GAMES
        # TODO - Create table "games", and change the parameters to be the ones that I want
        "INSERT INTO games (gamePk, gameType, season, gameDate) VALUES (%s, %s, %s, %s)",
        (gamePk, gameType, season, gameDate)
    )

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
