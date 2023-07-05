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
    print(lineup_stats)

    probables_stats = conn.execute("SELECT teamId, era FROM ProbablesStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(probables_stats)

    game_stats = conn.execute("SELECT teamId, teamWinPct FROM gamesv3 WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(game_stats)

    pitching_stats = conn.execute("SELECT teamId, strikeoutwalkratio FROM PitchingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(pitching_stats)

    pitching_stats2 = conn.execute("SELECT teamId, hitsper9inn FROM PitchingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(pitching_stats2)

    previous_pitching_stats = conn.execute("SELECT teamId, era FROM PreviousYearPitchingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(previous_pitching_stats)

    previous_pitching_stats2 = conn.execute("SELECT teamId, whip FROM PreviousYearPitchingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(previous_pitching_stats2)

    previous_hitting_stats = conn.execute("SELECT teamId, ops FROM PreviousYearHittingStats WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(previous_hitting_stats)

    team_names = conn.execute("SELECT teamId, teamname FROM Gamesv3 WHERE gameId = CAST(%s AS text)", (gameId,)).fetchall()
    print(team_names)

    # Perform the desired calculations for each team in the game
    teamOne = team_names[0][1] if len(team_names) > 0 else None
    teamTwo = team_names[1][1] if len(team_names) > 1 else None
    print(teamOne)
    print(teamTwo)


    countTeamOne = 0
    countTeamTwo = 0
    ops_hitting_team = []
    for _, ops_hitting in hitting_stats:
        ops_hitting_team.append(float(ops_hitting))
    print(ops_hitting_team)
    if ops_hitting_team[0] > ops_hitting_team[1]:
        countTeamOne += 1
    elif ops_hitting_team[1] > ops_hitting_team[0]:
        countTeamTwo += 1
    print(f"Count for Team One: {countTeamOne}")
    print(f"Count for Team Two: {countTeamTwo}")
                

    ops_lineup_team = []
    for _, ops_lineup in lineup_stats:
        ops_lineup_team.append(float(ops_lineup))
    print(ops_lineup_team)

    # Check if the lineup is not empty before comparing the values
    if len(ops_lineup_team) >= 2:        
        if ops_lineup_team[0] > ops_lineup_team[1]:
            countTeamOne += 1
        elif ops_lineup_team[1] > ops_lineup_team[0]:
            countTeamTwo += 1
    print(f"Count for Team One: {countTeamOne}")
    print(f"Count for Team Two: {countTeamTwo}")
                

    era_probables_team = []
    for _, era_probables in probables_stats:
        if era_probables is not None:
            era_probables_team.append(float(era_probables))
    if len(era_probables_team) >= 2:
        if era_probables_team[0] > era_probables_team[1]:
            countTeamOne += 3
        elif era_probables_team[1] > era_probables_team[0]:
            countTeamTwo += 3
        print(f"Count for Team One: {countTeamOne}")
        print(f"Count for Team Two: {countTeamTwo}")
                

    pct_team = []
    for _, pct in game_stats:
         pct_team.append(float(pct))
    if pct_team[0] > pct_team[1]:
        countTeamOne += 1
    elif pct_team[1] > pct_team[0]:
        countTeamTwo += 1
    print(f"Count for Team One: {countTeamOne}")
    print(f"Count for Team Two: {countTeamTwo}")
        

    strikeoutwalkratio_pitching_team = []
    for _, strikeoutwalkratio_pitching in pitching_stats:
        strikeoutwalkratio_pitching_team.append(float(strikeoutwalkratio_pitching))
    if strikeoutwalkratio_pitching_team[0] > strikeoutwalkratio_pitching_team[1]:
        countTeamOne += 1
    elif strikeoutwalkratio_pitching_team[1] > strikeoutwalkratio_pitching_team[0]:
        countTeamTwo += 1
    print(f"Count for Team One: {countTeamOne}")
    print(f"Count for Team Two: {countTeamTwo}")

    hitsper9inn_pitching_team = []
    for _, hitsper9inn_pitching in pitching_stats2:
        hitsper9inn_pitching_team.append(float(hitsper9inn_pitching))
    if hitsper9inn_pitching_team[0] > hitsper9inn_pitching_team[1]:
        countTeamOne += 1
    elif hitsper9inn_pitching_team[1] > hitsper9inn_pitching_team[0]:
        countTeamTwo += 1
    print(f"Count for Team One: {countTeamOne}")
    print(f"Count for Team Two: {countTeamTwo}")
                

    era_previous_pitching_team = []
    for _, era_previous_pitching in previous_pitching_stats:
        era_previous_pitching_team.append(float(era_previous_pitching))
    if len(era_previous_pitching_team) >= 2:
        if era_previous_pitching_team[0] > era_previous_pitching_team[1]:
            countTeamOne += 1
        elif era_previous_pitching_team[1] > era_previous_pitching_team[0]:
            countTeamTwo += 1
        print(f"Count for Team One: {countTeamOne}")
        print(f"Count for Team Two: {countTeamTwo}")
               
    whip_previous_pitching_team = []
    for _, whip_previous_pitching in previous_pitching_stats2:
        whip_previous_pitching_team.append(float(whip_previous_pitching))
    if len(whip_previous_pitching_team) >= 2:
        if whip_previous_pitching_team[0] > whip_previous_pitching_team[1]:
            countTeamOne += 1
        elif whip_previous_pitching_team[1] > whip_previous_pitching_team[0]:
            countTeamTwo += 1
        print(f"Count for Team One: {countTeamOne}")
        print(f"Count for Team Two: {countTeamTwo}")
               

    ops_previous_hitting_team = []
    for _, ops_previous_hitting in previous_hitting_stats:
        ops_previous_hitting_team.append(float(ops_previous_hitting))

    if len(ops_previous_hitting_team) >= 2:
        if ops_previous_hitting_team[0] > ops_previous_hitting_team[1]:
            countTeamOne += 1
        elif ops_previous_hitting_team[1] > ops_previous_hitting_team[0]:
            countTeamTwo += 1
        print(f"Count for Team One: {countTeamOne}")
        print(f"Count for Team Two: {countTeamTwo}")
                

    if countTeamOne > countTeamTwo:
        predicted_winner = teamOne
    elif countTeamTwo > countTeamOne:
        predicted_winner = teamTwo
    else:
        predicted_winner = teamTwo  # Tie or no winner

    # Update the 'games' table with the predicted winner
    conn.execute("UPDATE games SET predictedWinner5 = %s WHERE gameId = CAST(%s AS text)", (predicted_winner, str(gameId)))
    print(f"GameId: {gameId} - Winner prediction stored in the database.")
    
# Close the connection
conn.close()
print("Database connection closed.")