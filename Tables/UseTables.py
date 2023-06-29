from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
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

    # Check if current_data_imputed is not empty
    if not current_data_imputed.empty:
        # Use the trained model to predict the winner of current date games
        X_current = current_data_imputed.values
        current_data["predicted_winner"] = model.predict(X_current)

        print("Column names in current_data:")
        print(current_data.columns)

        # Store the predicted winners in the database
        current_data["predicted_winner"] = current_data["predicted_winner"].map({1: current_data["teamname"], 2: current_data["team_name"]})
        predicted_winners = current_data["predicted_winner"].tolist()

        for predicted_winner in predicted_winners:
            update_query = f"UPDATE games SET predictedWinner = '{predicted_winner}' WHERE gameId = {gameId}"
            engine.execute(update_query)

        print(f"GameId: {gameId} - Winner prediction stored in the database.")
    else:
        print(f"GameId: {gameId} - No valid data available for prediction.")

# Close the database connection
engine.dispose()














# from sqlalchemy import create_engine
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.impute import SimpleImputer

# # Create a SQLAlchemy engine
# engine = create_engine('postgresql://syabkhtb:J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE@rajje.db.elephantsql.com:5432/syabkhtb')

# # Fetch the historical data from the database tables
# query = "SELECT * FROM PitchingStats2022"
# pitching_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM probablesStats2022"
# probables_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM previousYearPitchingStats2022"
# previous_pitching_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM previousYearHittingStats2022"
# previous_hitting_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM lineupStats2022"
# lineup_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM HittingStats2022"
# hitting_stats_df = pd.read_sql_query(query, engine)

# # Merge the relevant historical tables based on common keys
# historical_data = pd.merge(pitching_stats_df, probables_stats_df, on=["gameid"], how="inner", suffixes=('_pitching', '_probables'))
# historical_data = pd.merge(historical_data, previous_pitching_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_pitching'))
# historical_data = pd.merge(historical_data, previous_hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_previous_hitting'))
# historical_data = pd.merge(historical_data, lineup_stats_df, on=["gameid"], how="inner", suffixes=('', '_lineup'))
# historical_data = pd.merge(historical_data, hitting_stats_df, on=["gameid"], how="inner", suffixes=('', '_hitting'))

# # Adjust the features list to include the correct column names
# features = ["era", "whip", "hitsper9inn", "runsscoredper9", "homerunsper9",
#             "strikeoutwalkratio_pitching", "games_started", "gamespitched", "strikeouts", "saves", "blownsaves",
#             "obp", "slg_hitting", "ops", "strikeoutwalkratio_probables",
#             "at_bats_per_home_run", "babip"]
# target = "iswinner"

# # Replace non-numeric values with NaN
# historical_data[features] = historical_data[features].apply(pd.to_numeric, errors='coerce')

# X = historical_data[features]
# y = historical_data[target]

# # Preprocess the data to handle missing values
# imputer = SimpleImputer(strategy='mean')
# X_imputed = imputer.fit_transform(X)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# # Train the logistic regression model
# model = LogisticRegression(max_iter=2000)
# model.fit(X_train, y_train)

# # Fetch the current date data from the database tables
# query = "SELECT * FROM PitchingStats"
# current_pitching_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM probablesStats"
# current_probables_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM previousYearPitchingStats"
# current_previous_pitching_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM previousYearHittingStats"
# current_previous_hitting_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM lineupStats"
# current_lineup_stats_df = pd.read_sql_query(query, engine)

# query = "SELECT * FROM HittingStats"
# current_hitting_stats_df = pd.read_sql_query(query, engine)

# # Merge the relevant current date tables based on common keys
# current_data = pd.merge(current_pitching_stats_df, current_probables_stats_df, on=["gameid"], how="left", suffixes=('_pitching', '_probables'))
# current_data = pd.merge(current_data, current_previous_pitching_stats_df, on=["gameid"], how="left", suffixes=('', '_previous_pitching'))
# current_data = pd.merge(current_data, current_previous_hitting_stats_df, on=["gameid"], how="left", suffixes=('', '_previous_hitting'))
# current_data = pd.merge(current_data, current_lineup_stats_df, on=["gameid"], how="left", suffixes=('', '_lineup'))
# current_data = pd.merge(current_data, current_hitting_stats_df, on=["gameid"], how="left", suffixes=('', '_hitting'))

# print("Current Data:")
# print(current_data.head())

# # Fill missing values with column means
# numeric_columns = ["era", "whip", "hitsper9inn", "runsscoredper9", "homerunsper9",
#                    "strikeoutwalkratio_pitching", "games_started", "gamespitched", "strikeouts", "saves", "blownsaves",
#                    "obp", "slg_hitting", "ops", "strikeoutwalkratio_probables",
#                    "at_bats_per_home_run", "babip"]
# current_data[numeric_columns] = current_data[numeric_columns].fillna(current_data[numeric_columns].mean(numeric_only=True))


# # Check for missing values in the current_data dataframe
# missing_values = current_data[features].isnull().sum()
# print(missing_values)

# # Handle missing values in the current_data DataFrame
# current_data[features] = current_data[features].apply(pd.to_numeric, errors='coerce')
# current_data_imputed = imputer.transform(current_data[features])

# # Check if current_data is not empty and has no missing values
# if not current_data.empty:
#     # Preprocess the current date data
#     X_current = imputer.transform(current_data[features])

#     # Use the trained model to predict the winner of current date games
#     current_data["predicted_winner"] = model.predict(X_current)

#     # Store the predicted winners in the database
#     for index, row in current_data.iterrows():
#         gameId = row["gameid"]
#         predicted_winner = row["predicted_winner"]

#         update_query = f"UPDATE games SET predictedWinner = {predicted_winner} WHERE gameid = {gameId}"
#         engine.execute(update_query)

#     print("Predictions have been stored in the database.")
# else:
#     print("No valid data available for prediction.")

# # Close the database connection
# engine.dispose()