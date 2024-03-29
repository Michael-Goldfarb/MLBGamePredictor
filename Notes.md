# How to set up the database!
Make an account on ElephantSQL, create an instance, click on browser, then copy and paste these 17 create table statements individually in ElephantSQL before running the program files!
Make sure to follow the instructions on the bottom of the page after creating the 17 tables!


 1.     CREATE TABLE IF NOT EXISTS gamesRefresh (
        gameId TEXT,
        awayTeamName VARCHAR(255),
        homeTeamName VARCHAR(255),
        gameStatus VARCHAR(255),
        gameDate DATE,
        gameTime TIME,
        awayTeamScore INTEGER,
        homeTeamScore INTEGER,
        awayTeamWinPct FLOAT,
        homeTeamWinPct FLOAT,
        venue VARCHAR(255),
        isWinnerAway BOOLEAN,
        isWinnerHome BOOLEAN,
        featuredWinner VARCHAR(255),
        correct BOOLEAN,
        currentInning VARCHAR(255),
        inningHalf VARCHAR(255)

        )


3.     CREATE TABLE IF NOT EXISTS gamesv3 (
        gameId TEXT,
        link VARCHAR(255),
        teamId INTEGER,
        teamName VARCHAR(255),
        gameStatus VARCHAR(255),
        gameDate DATE,
        gameTime TIME,
        teamScore INTEGER,
        teamWinPct FLOAT,
        venue VARCHAR(255),
        isWinner BOOLEAN,
        predictedWinner VARCHAR(255),
        predictedWinner2 VARCHAR(255),
        predictedWinner3 VARCHAR(255),
        predictedWinner4 VARCHAR(255),
        predictedWinner5 VARCHAR(255)
       )


4.     CREATE TABLE IF NOT EXISTS HittingStats (
        gameId TEXT,
        teamId INTEGER,
        team_name VARCHAR(255),
        runs INTEGER,
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPlayed INTEGER,
        leftOnBase INTEGER,
        stolenBases INTEGER
       )



5.     CREATE TABLE IF NOT EXISTS lineupStats (
        gameId TEXT,
        teamId TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        games_played INTEGER,
        babip TEXT
       )



6.     CREATE TABLE IF NOT EXISTS PitchingStats (
        teamId INTEGER,
        gameId TEXT,
        team_name VARCHAR(255),
        era VARCHAR(255),
        whip VARCHAR(255),
        hitsPer9Inn VARCHAR(255),
        runsScoredPer9 VARCHAR(255),
        homeRunsPer9 VARCHAR(255),
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPitched INTEGER,
        strikeOuts INTEGER,
        saves INTEGER,
        blownSaves INTEGER,
        strikeoutWalkRatio VARCHAR(255)
       )




7.     CREATE TABLE IF NOT EXISTS previousYearHittingStats (
        gameId TEXT,
        teamId TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        games_played INTEGER,
        babip TEXT
       )



8.     CREATE TABLE IF NOT EXISTS previousYearPitchingStats (
        player_id TEXT,
        gameId TEXT,
        teamId TEXT,
        player_name TEXT,
        strikeoutWalkRatio TEXT,
        games_started INTEGER,
        hitsPer9Inn TEXT,
        strikeoutsPer9Inn TEXT,
        team_name TEXT,
        era TEXT,
        whip TEXT,
        walksPer9Inn TEXT
       )



9.     CREATE TABLE IF NOT EXISTS probablesStats (
        player_id TEXT,
        gameId TEXT,
        teamId VARCHAR(255),
        player_name TEXT,
        strikeoutWalkRatio TEXT,
        games_started INTEGER,
        hitsPer9Inn TEXT,
        strikeoutsPer9Inn TEXT,
        team_name TEXT,
        era TEXT,
        whip TEXT,
        walksPer9Inn TEXT
       )




10.     CREATE TABLE IF NOT EXISTS games (
        gameId TEXT,
        awayTeamId INTEGER,
        homeTeamId INTEGER,
        awayTeamName VARCHAR(255),
        homeTeamName VARCHAR(255),
        awayTeamScore INTEGER,
        homeTeamScore INTEGER,
        awayTeamWinPct FLOAT,
        homeTeamWinPct FLOAT,
        isWinnerAway BOOLEAN,
        isWinnerHome BOOLEAN,
        predictedWinner VARCHAR(255),
        predictedWinner2 VARCHAR(255),
        predictedWinner3 VARCHAR(255),
        predictedWinner4 VARCHAR(255),
        predictedWinner5 VARCHAR(255),
        earlyWinner VARCHAR(255),
        theWinner VARCHAR(255),
        featuredWinner VARCHAR(255),
        correct BOOLEAN
       )





11.     CREATE TABLE IF NOT EXISTS teamRecords (
        teamName VARCHAR(255),
        numerator INTEGER,
        denominator INTEGER,
        percentage FLOAT,
        insertedYet VARCHAR(255)
        )





12.     CREATE TABLE IF NOT EXISTS dailyPredictions (
         prediction_date DATE PRIMARY KEY,
         numerator INTEGER,
         denominator INTEGER
        );




13.     CREATE TABLE IF NOT EXISTS HittingStats2022v3 (
        teamId INTEGER,
        gameId VARCHAR(255),
        gameDate DATE,
        teamName VARCHAR(255),
        runs INTEGER,
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPlayed INTEGER,
        leftOnBase INTEGER,
        stolenBases INTEGER,
        isWinner BOOLEAN
        )



14.     CREATE TABLE IF NOT EXISTS lineupStats2022v3 (
            date DATE,
            gameId TEXT,
            teamId TEXT,
            obp TEXT,
            slg TEXT,
            ops TEXT,
            at_bats_per_home_run TEXT,
            games_played INTEGER,
            babip TEXT,
            isWinner BOOLEAN
        )




15.     CREATE TABLE IF NOT EXISTS PitchingStats2022v3 (
        teamId INTEGER,
        gameId TEXT,
        gameDate DATE,
        teamName VARCHAR(255),
        era VARCHAR(255),
        whip VARCHAR(255),
        hitsPer9Inn VARCHAR(255),
        runsScoredPer9 VARCHAR(255),
        homeRunsPer9 VARCHAR(255),
        obp VARCHAR(255),
        slg VARCHAR(255),
        ops VARCHAR(255),
        gamesPitched INTEGER,
        strikeOuts INTEGER,
        saves INTEGER,
        blownSaves INTEGER,
        strikeoutWalkRatio VARCHAR(255),
        isWinner BOOLEAN
        )



16.     CREATE TABLE IF NOT EXISTS previousYearHittingStats2022v3 (
        date DATE,
        teamId TEXT,
        gameId TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        games_played INTEGER,
        babip TEXT,
        isWinner BOOLEAN
        )



17.     CREATE TABLE IF NOT EXISTS previousYearPitchingStats2022V3 (
            player_id TEXT,
            gameDate DATE,
            gameId TEXT,
            teamId TEXT,
            player_name TEXT,
            strikeoutWalkRatio TEXT,
            games_started INTEGER,
            hitsPer9Inn TEXT,
            strikeoutsPer9Inn TEXT,
            team_name TEXT,
            era TEXT,
            whip TEXT,
            walksPer9Inn TEXT,
            isWinner BOOLEAN
        )



18.     CREATE TABLE IF NOT EXISTS probablesStats2022V3 (
            player_id TEXT,
            gameDate DATE,
            gameId TEXT,
            teamId TEXT,
            player_name TEXT,
            strikeoutWalkRatio TEXT,
            games_started INTEGER,
            hitsPer9Inn TEXT,
            strikeoutsPer9Inn TEXT,
            team_name TEXT,
            era TEXT,
            whip TEXT,
            walksPer9Inn TEXT,
            isWinner BOOLEAN
        )

## Once you have copied and pasted each statement, run this statement in your terminal: (replace [REPLACE] with your database credentials)!

    export DB_HOST=[REPLACE] 
    export DB_NAME=[REPLACE]
    export DB_USER=[REPLACE] 
    export DB_PORT=5432
    export DB_PASSWORD=[REPLACE]

Note that all of this information can be found in the 'details' section of your instance. DB_HOST is 'Server', DB_NAME and DB_USER is 'User & Default database', and DB_PASSWORD is 'Password'
Keep this information stored somewhere because you will need it for future use.



Afterwards, to get information properly in the database, open up a new terminal, cd into MLBGamePredictor, then run these statments:
1.     git checkout backend
2.     export DB_HOST=[REPLACE] 
       export DB_NAME=[REPLACE]
       export DB_USER=[REPLACE] 
       export DB_PORT=5432
       export DB_PASSWORD=[REPLACE]
3.     cd Tables
4.     cd PastTables
5.     python HittingStats2022.py
6.     python PitchingStats2022.py
7.     python LineupStats2022.py
8.     python PreviousYearPitchingStats2022.py
9.     python PreviousYearHittingStats2022.py
10.     python ProbablesStats2022.py
   
(#2 is the same statement you just created (make sure to replace the [REPLACE] parts))

Email me @ michaelgoldfarb6@gmail.com if you run into any difficulties or have any questions! Note that it may take a while to load the data into the database.
