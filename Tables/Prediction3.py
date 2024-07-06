from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
import os
from collections import Counter

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_port = os.environ.get('DB_PORT')
db_password = os.environ.get('DB_PASSWORD')

# Use the variables in your create_engine() call:
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Fetch the historical data from the database tables
query = "SELECT * FROM PitchingStats2022v3"
pitching_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM probablesStats2022v3"
probables_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM previousYearPitchingStats2022v3"
previous_pitching_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM previousYearHittingStats2022v3"
previous_hitting_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM lineupStats2022v3"
lineup_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM HittingStats2022v3"
hitting_stats_df = pd.read_sql_query(query, engine)

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

# Train the logistic regression model (only if the model hasn't been trained and saved before)
model_filename = "logistic_regression_model.pkl"

try:
    # Load the trained model
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    print("Trained model loaded from file.")
except FileNotFoundError:
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

    # Train the model if the saved model file is not found
    print("Training model...")
    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)
    print("Trained model saved to file.")

# Fetch the gameIds from the 'games' table
query = "SELECT gameId FROM games"
gameIds = pd.read_sql_query(query, engine)["gameid"].tolist()
print(gameIds)

# Iterate over each gameId
for gameId in gameIds:
    # Fetch the current date data from the database tables for the current gameId
    query = f"SELECT * FROM PitchingStats WHERE gameid = '{gameId}'"
    current_pitching_stats_df = pd.read_sql_query(query, engine)

    query = f"SELECT * FROM probablesStats WHERE gameid = '{gameId}'"
    current_probables_stats_df = pd.read_sql_query(query, engine)

    query = f"SELECT * FROM previousYearPitchingStats WHERE gameid = '{gameId}'"
    current_previous_pitching_stats_df = pd.read_sql_query(query, engine)

    query = f"SELECT * FROM previousYearHittingStats WHERE gameid = '{gameId}'"
    current_previous_hitting_stats_df = pd.read_sql_query(query, engine)

    query = f"SELECT * FROM lineupStats WHERE gameid = '{gameId}'"
    current_lineup_stats_df = pd.read_sql_query(query, engine)

    query = f"SELECT * FROM HittingStats WHERE gameid = '{gameId}'"
    current_hitting_stats_df = pd.read_sql_query(query, engine)

    # Merge the relevant current date tables based on common keys
    current_data = pd.merge(current_pitching_stats_df, current_probables_stats_df, on=["gameid"], how="left", suffixes=('_pitching', '_probables'))
    current_data = pd.merge(current_data, current_previous_pitching_stats_df, on=["gameid"], how="left", suffixes=('', '_previous_pitching'))
    current_data = pd.merge(current_data, current_previous_hitting_stats_df, on=["gameid"], how="left", suffixes=('', '_previous_hitting'))
    current_data = pd.merge(current_data, current_lineup_stats_df, on=["gameid"], how="left", suffixes=('', '_lineup'))
    current_data = pd.merge(current_data, current_hitting_stats_df, on=["gameid"], how="left", suffixes=('', '_hitting'))

    # Handle missing values in the current_data DataFrame
    current_data[features] = current_data[features].apply(pd.to_numeric, errors='coerce')
    current_data_imputed = imputer.transform(current_data[features])

    # Convert imputed data back to DataFrame
    current_data_imputed = pd.DataFrame(current_data_imputed, columns=features)

    # Ensure there are no empty predictions
    if current_data_imputed.empty:
        print(f"GameId: {gameId} - No valid data available for prediction.")
        continue  # Skip to the next iteration of the loop

    # Use the trained model to predict the winner of current date games
    X_current = current_data_imputed.values

    # Get probabilities and apply threshold
    threshold = 0.3  # Adjust this threshold as needed
    probabilities = model.predict_proba(X_current)[:, 1]
    current_data["predicted_winner"] = (probabilities >= threshold).astype(int)

    # Reset the index of the current_data DataFrame
    current_data.reset_index(drop=True, inplace=True)

    # Store the predicted winners in the database
    predicted_winner_team_ids = current_data.loc[current_data["predicted_winner"] == 1, "teamid"].values

    if predicted_winner_team_ids.size > 0:
        most_common_team_id = Counter(predicted_winner_team_ids).most_common(1)[0][0]
    else:
        most_common_team_id = None

    if most_common_team_id is not None:
        # Fetch the team names and IDs from the 'games' table for the current gameId
        query = f"SELECT hometeamid, awayteamid, hometeamname, awayteamname FROM games WHERE gameId = '{gameId}'"
        game_info = pd.read_sql_query(query, engine)

        hometeamid = game_info["hometeamid"].values[0]
        awayteamid = game_info["awayteamid"].values[0]
        hometeamname = game_info["hometeamname"].values[0]
        awayteamname = game_info["awayteamname"].values[0]

        # Determine the team name based on the most common team ID
        if most_common_team_id == str(hometeamid):
            predicted_winner_team_name = hometeamname
        elif most_common_team_id == str(awayteamid):
            predicted_winner_team_name = awayteamname
        else:
            predicted_winner_team_name = None

        if predicted_winner_team_name is not None:
            update_query = "UPDATE games SET predictedWinner3 = %s WHERE gameId = %s"
            try:
                engine.execute(update_query, (predicted_winner_team_name, gameId))
                print(f"GameId: {gameId} - Winner prediction stored in the database.")
            except Exception as e:
                # Handle any exceptions that occur during the execution
                print("An error occurred during update:", str(e))

# Close the database connection
engine.dispose()
print("Database connection closed.")
