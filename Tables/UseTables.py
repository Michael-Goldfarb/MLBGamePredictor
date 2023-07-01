from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

# Create a SQLAlchemy engine
engine = create_engine('postgresql://syabkhtb:J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE@rajje.db.elephantsql.com:5432/syabkhtb')

# Fetch the historical data from the database tables
query = "SELECT * FROM PitchingStats2022"
pitching_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM probablesStats2022"
probables_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM previousYearPitchingStats2022"
previous_pitching_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM previousYearHittingStats2022v2"
previous_hitting_stats_df = pd.read_sql_query(query, engine)

query = "SELECT * FROM lineupStats2022v2"
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

# Preprocess the data to handle missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

model_filename = "HistGradientBoostingClassifier.pkl"

if os.path.isfile(model_filename):
    # Load the trained model
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    print("Trained model loaded from file.")
else:
    print("Training model...")
    model = HistGradientBoostingClassifier()
    model.fit(X_train, y_train)
    print("Training Accuracy:", model.score(X_train, y_train))
    print("Testing Accuracy:", model.score(X_test, y_test))
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
    current_data = pd.merge(current_pitching_stats_df, current_probables_stats_df, on=["gameid"], how="inner", suffixes=('_pitching', '_probables'))
    current_data = pd.merge(current_data, current_previous_pitching_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_pitching'))
    current_data = pd.merge(current_data, current_previous_hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_hitting'))
    current_data = pd.merge(current_data, current_lineup_stats_df, on=["gameid"], how="inner", suffixes=('', '_lineup'))
    current_data = pd.merge(current_data, current_hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_hitting'))

    # Check if the current_data DataFrame has at least one sample
    if not current_data.empty:
        # Calculate the mean values from the training data
        mean_values = X_train.mean()

        # Predict winner
        X_current = current_data[features]
        current_data["predicted_winner"] = model.predict(X_current)

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
    else:
        # Handle the case when current_data is empty (no samples available)
        updated_data.append(("Unknown", gameId))
        print(f"GameId: {gameId} - Missing data, prediction marked as unknown.")

# Prepare the query to update all rows at once
update_query = "UPDATE games SET predictedWinner = %(winner)s WHERE gameId = %(gameId)s"

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