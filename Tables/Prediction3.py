from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
import os

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_port = os.environ.get('DB_PORT')
db_password = os.environ.get('DB_PASSWORD')

# Use the variables in your create_engine() call:
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Fetch the historical data from the database tables
query = "SELECT * FROM PitchingStats2022"
pitching_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM probablesStats2022"
probables_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM previousYearPitchingStats2022"
previous_pitching_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM previousYearHittingStats2022"
previous_hitting_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM lineupStats2022"
lineup_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM HittingStats2022"
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

# Create a list to store the updated data
updated_data = []

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

    # Drop rows with missing values
    current_data_imputed = pd.DataFrame(current_data_imputed, columns=features)
    current_data_imputed.dropna(inplace=True)

    print(gameId)

    # Check if current_data_imputed is not empty
    if current_data_imputed.empty:
        print(f"GameId: {gameId} - No valid data available for prediction.")
        continue  # Skip to the next iteration of the loop

    # Use the trained model to predict the winner of current date games
    X_current = current_data_imputed.values
    current_data["predicted_winner"] = model.predict(X_current)

    # Reset the index of the current_data DataFrame
    current_data.reset_index(drop=True, inplace=True)

    # Store the predicted winners in the database
    current_data.loc[current_data["predicted_winner"] == 1, "predicted_winner"] = current_data["teamid"]

    # Map team IDs to team names (or appropriate identifiers) using a dictionary
    team_id_to_name = {
        team_id: team_name for team_id, team_name in zip(current_data["teamid"], current_data["team_name"])
    }

     # Get the predicted winners as a list of team names
    predicted_winners = current_data["predicted_winner"].map(team_id_to_name)
        
    # Add the gameId and predicted winners to the updated_data list
    updated_data.extend([(winner, gameId) for winner, gameId in zip(predicted_winners, current_data["gameid"])])

    print(f"GameId: {gameId} - Winner prediction stored in the database.")

# Prepare the query to update all rows at once
update_query = "UPDATE games SET predictedWinner3 = %(winner)s WHERE gameId = %(gameId)s"

# Convert the updated_data list into a dictionary
parameters = [{'winner': winner, 'gameId': gameId} for winner, gameId in updated_data]

try:
    # Execute the bulk update query
    engine.execute(update_query, parameters)
    print("Bulk update query executed.")
except Exception as e:
    # Handle any exceptions that occur during the execution
    print("An error occurred during bulk update:", str(e))
finally:
    # Close the database connection
    engine.dispose()
    print("Database connection closed.")