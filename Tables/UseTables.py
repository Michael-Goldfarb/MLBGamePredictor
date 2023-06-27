import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Connect to ElephantSQL database
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)

# Fetch the historical data from the database tables
query = "SELECT * FROM PitchingStats2022"
pitching_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM probablesStats2022"
probables_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM previousYearPitchingStats2022"
previous_pitching_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM previousYearHittingStats2022"
previous_hitting_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM lineupStats2022"
lineup_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM LineupAndProbables2022"
lineup_probables_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM HittingStats2022"
hitting_stats_df = pd.read_sql_query(query, conn)

# Merge the relevant historical tables based on common keys
historical_data = pd.merge(pitching_stats_df, probables_stats_df, on=["gameId"], how="inner")
historical_data = pd.merge(historical_data, previous_pitching_stats_df, on=["gameId"], how="inner")
historical_data = pd.merge(historical_data, previous_hitting_stats_df, on=["gameId"], how="inner")
historical_data = pd.merge(historical_data, lineup_stats_df, on=["gameId"], how="inner")
historical_data = pd.merge(historical_data, lineup_probables_df, on=["gameId"], how="inner")
historical_data = pd.merge(historical_data, hitting_stats_df, on=["gameId"], how="inner")

# Prepare the data for training the machine learning model
features = ["era", "whip", "hitsPer9Inn", "runsScoredPer9", "homeRunsPer9", "strikeoutWalkRatio", "games_started", "gamesPitched", "strikeOuts", "saves", "blownSaves", "obp", "slg", "ops", "strikeoutWalkRatio", "at_bats_per_home_run"]
target = "isWinner"

X = historical_data[features]
y = historical_data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the machine learning model
model = LogisticRegression()
model.fit(X_train, y_train)

# Fetch the current date data from the database tables
query = "SELECT * FROM PitchingStats"
current_pitching_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM probablesStats"
current_probables_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM previousYearPitchingStats"
current_previous_pitching_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM previousYearHittingStats"
current_previous_hitting_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM lineupStats"
current_lineup_stats_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM LineupAndProbables"
current_lineup_probables_df = pd.read_sql_query(query, conn)

query = "SELECT * FROM HittingStats"
current_hitting_stats_df = pd.read_sql_query(query, conn)

# Merge the relevant current date tables based on common keys

current_data = pd.merge(current_pitching_stats_df, current_probables_stats_df, on=["gameId"], how="inner")
current_data = pd.merge(current_data, current_previous_pitching_stats_df, on=["gameId"], how="inner")
current_data = pd.merge(current_data, current_previous_hitting_stats_df, on=["gameId"], how="inner")
current_data = pd.merge(current_data, current_lineup_stats_df, on=["gameId"], how="inner")
current_data = pd.merge(current_data, current_lineup_probables_df, on=["gameId"], how="inner")
current_data = pd.merge(current_data, current_hitting_stats_df, on=["gameId"], how="inner")

# Use the trained model to predict the winner of current date games

X_current = current_data[features]
current_data["predicted_winner"] = model.predict(X_current)

# Store the predicted winners in the database
for index, row in current_data.iterrows():
    gameId = row["gameId"]
    predicted_winner = row["predicted_winner"]
    
    update_query = f"UPDATE games SET predictedWinner = {predicted_winner} WHERE gameId = {gameId}"
    with conn.cursor() as cursor:
        cursor.execute(update_query)
    conn.commit()

# Close the database connection
conn.close()