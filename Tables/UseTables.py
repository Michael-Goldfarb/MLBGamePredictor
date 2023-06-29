import psycopg2
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer

# Connect to ElephantSQL database
conn = psycopg2.connect(
    host='rajje.db.elephantsql.com',
    database='syabkhtb',
    user='syabkhtb',
    port='5432',
    password='J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
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

query = "SELECT * FROM HittingStats2022"
hitting_stats_df = pd.read_sql_query(query, conn)

# Merge the relevant historical tables based on common keys
historical_data = pd.merge(pitching_stats_df, probables_stats_df, on=["gameid"], how="inner", suffixes=('_pitching', '_probables'))
historical_data = pd.merge(historical_data, previous_pitching_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_pitching'))
historical_data = pd.merge(historical_data, previous_hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_hitting'))
historical_data = pd.merge(historical_data, lineup_stats_df, on=["gameid"], how="inner", suffixes=('', '_lineup'))
historical_data = pd.merge(historical_data, hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_hitting'))

# Adjust the features list to include the correct column names
features = ["era", "whip", "hitsper9inn", "runsscoredper9", "homerunsper9",
            "strikeoutwalkratio_pitching", "games_started", "gamespitched", "strikeouts", "saves", "blownsaves",
            "obp", "slg_hitting", "ops", "strikeoutwalkratio_probables",
            "at_bats_per_home_run", "babip"]
target = "iswinner"

# Replace non-numeric values with NaN
historical_data[features] = historical_data[features].apply(pd.to_numeric, errors='coerce')

X = historical_data[features]
y = historical_data[target]

# Preprocess the data to handle missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Train the logistic regression model
model = LogisticRegression(max_iter=1000)
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

query = "SELECT * FROM HittingStats"
current_hitting_stats_df = pd.read_sql_query(query, conn)

# Merge the relevant current date tables based on common keys
current_data = pd.merge(current_pitching_stats_df, current_probables_stats_df, on=["gameid"], how="inner", suffixes=('_pitching', '_probables'))
current_data = pd.merge(current_data, current_previous_pitching_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_pitching'))
current_data = pd.merge(current_data, current_previous_hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_hitting'))
current_data = pd.merge(current_data, current_lineup_stats_df, on=["gameid"], how="inner", suffixes=('', '_lineup'))
current_data = pd.merge(current_data, current_hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_hitting'))
if not current_data.empty:
    current_data[features] = current_data[features].apply(pd.to_numeric, errors='coerce')

    # Preprocess the current date data
    X_current = imputer.transform(current_data[features])

    # Use the trained model to predict the winner of current date games
    current_data["predicted_winner"] = model.predict(X_current)

    # Store the predicted winners in the database
    for index, row in current_data.iterrows():
        gameId = row["gameid"]
        predicted_winner = row["predicted_winner"]

        update_query = f"UPDATE games SET predictedWinner = {predicted_winner} WHERE gameid = {gameId}"
        with conn.cursor() as cursor:
            cursor.execute(update_query)
        conn.commit()


# Close the database connection
conn.close()
