from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from collections import Counter

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_port = os.environ.get('DB_PORT')
db_password = os.environ.get('DB_PASSWORD')

# Use the variables in your create_engine() call:
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

scaler = StandardScaler()

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
features = ["era_probables", "era_pitching", "era", "whip_pitching", "whip_probables", "whip",
             "hitsper9inn_pitching", "hitsper9inn_probables", "hitsper9inn", "runsscoredper9", "homerunsper9",
            "strikeoutwalkratio_pitching", "games_started", "gamespitched", "strikeouts", "saves", "blownsaves", "strikeoutwalkratio_probables",
            "obp_hitting", "slg_hitting", "ops_hitting", "strikeoutwalkratio", "ops_lineup", "obp_lineup", "slg_lineup", "babip_lineup",
            "babip", "ops_previous_hitting", "obp_previous_hitting", "slg_previous_hitting"
            ]
target = "iswinner"

# Replace "-.--" with NaN
historical_data.replace("-.--", np.nan, inplace=True)

# Drop rows with unknown labels and NaN values
unknown_labels = historical_data[target] == 'unknown'
historical_data = historical_data[~unknown_labels]

X = historical_data[features]
y = historical_data[target].astype(bool)

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier())
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_filename = "RandomForestModelv5.pkl"

if os.path.isfile(model_filename):
    # Load the trained model
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    print("Trained model loaded from file.")
else:
    print("Training model...")
    model = pipeline.fit(X_train, y_train)
    print("Training Accuracy:", model.score(X_train, y_train))
    print("Testing Accuracy:", model.score(X_test, y_test))
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)
    print("Trained model saved to file.")

# Fetch the gameIds from the 'games' table
query = "SELECT gameId FROM games"
gameIds = pd.read_sql_query(query, engine)["gameid"].tolist()

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
    current_data = pd.merge(current_pitching_stats_df, current_probables_stats_df, on=["gameid"], how="inner", suffixes=('_pitching', '_probables'))
    current_data = pd.merge(current_data, current_previous_pitching_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_pitching'))
    current_data = pd.merge(current_data, current_previous_hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_hitting'))
    current_data = pd.merge(current_data, current_lineup_stats_df, on=["gameid"], how="left", suffixes=('', '_lineup'))
    current_data = pd.merge(current_data, current_hitting_stats_df, on=["gameid"], how="left", suffixes=('', '_hitting'))

    # Check if the current_data DataFrame has at least one sample
    if not current_data.empty:
        # Predict winner
        X_current = current_data[features]
        current_data["predicted_proba"] = model.predict_proba(X_current)[:, 1]

        # Apply the threshold of 0.30
        current_data["predicted_winner"] = (current_data["predicted_proba"] >= 0.30).astype(int)

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
                update_query = "UPDATE games SET predictedWinner = %s WHERE gameId = %s"
                try:
                    engine.execute(update_query, (predicted_winner_team_name, gameId))
                    print(f"GameId: {gameId} - Winner prediction stored in the database.")
                except Exception as e:
                    # Handle any exceptions that occur during the execution
                    print("An error occurred during update:", str(e))
    else:
        print(f"GameId: {gameId} - No valid data available for prediction.")

# Close the database connection
engine.dispose()
print("Database connection closed.")
