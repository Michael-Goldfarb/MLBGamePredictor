from sqlalchemy import create_engine

# Set up connection to ElephantSQL using SQLAlchemy
engine = create_engine('postgresql://syabkhtb:J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE@rajje.db.elephantsql.com:5432/syabkhtb')
conn = engine.connect()

# Fetch the gameIds from the 'games' table
gameIds = conn.execute("SELECT gameId FROM games").fetchall()

# Create a list to store the updated data
updated_data = []

# Iterate over each gameId
for gameId in gameIds:
    # Convert gameId to an integer
    gameId = int(gameId[0])

    # Fetch the current data from the relevant tables for the current gameId
    hitting_stats = conn.execute("SELECT teamId, ops FROM HittingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(hitting_stats)

    lineup_stats = conn.execute("SELECT teamId, ops FROM LineupStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()

    probables_stats = conn.execute("SELECT teamId, era FROM ProbablesStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()

    game_stats = conn.execute("SELECT teamId, teamWinPct FROM gamesv3 WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()

    pitching_stats = conn.execute("SELECT teamId, strikeoutwalkratio, hitsper9inn FROM PitchingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()

    previous_pitching_stats = conn.execute("SELECT teamId, era, whip FROM PreviousYearPitchingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()

    previous_hitting_stats = conn.execute("SELECT teamId, ops FROM PreviousYearHittingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()

    # Perform the desired calculations for each team in the game
    count = {teamId: 0 for teamId in [game_stats[0][0], game_stats[0][1]]}
    for teamId in [game_stats[0][0], game_stats[0][1]]:
        for _, ops_hitting in hitting_stats:
            if float(ops_hitting) > count[teamId]:
                print(float(ops_hitting))
                print(count[teamId])
                count[teamId] = float(ops_hitting)
                

        for _, ops_lineup in lineup_stats:
            if float(ops_lineup) > count[teamId]:
                count[teamId] = float(ops_lineup)
                

        for _, era_probables in probables_stats:
            if era_probables is not None and float(era_probables) < count[teamId]:
                count[teamId] = float(era_probables)
                

        for _, pct in game_stats:
            if float(pct) > count[teamId]:
                count[teamId] = float(pct)
                

        for _, strikeoutwalkratio_pitching, hitsper9inn_pitching in pitching_stats:
            if float(strikeoutwalkratio_pitching) > count[teamId]:
                count[teamId] = float(strikeoutwalkratio_pitching)
                
            if float(hitsper9inn_pitching) < count[teamId]:
                count[teamId] = float(hitsper9inn_pitching)
                

        for _, era_previous_pitching, whip_previous_pitching in previous_pitching_stats:
            if float(era_previous_pitching) < count[teamId]:
                count[teamId] = float(era_previous_pitching)
               
            if float(whip_previous_pitching) < count[teamId]:
                count[teamId] = float(whip_previous_pitching)
               

        for _, ops_previous_hitting in previous_hitting_stats:
            if float(ops_previous_hitting) > count[teamId]:
                count[teamId] = float(ops_previous_hitting)
                

    # Determine the predicted winner based on the calculated values
    predicted_winner = max(count, key=count.get)

    # Update the 'games' table with the predicted winner
    conn.execute("UPDATE games SET predictedWinner5 = %s WHERE gameId = CAST(%s AS text)", (predicted_winner, str(gameId)))
    updated_data.append((predicted_winner, gameId))
    print(f"GameId: {gameId} - Winner prediction stored in the database.")

# Close the connection
conn.close()
print("Database connection closed.")
