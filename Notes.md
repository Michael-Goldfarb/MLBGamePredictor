# Make an account on ElephantSQL, create an instance, click on browser, then copy and paste these create table statements in ElephantSQL before running the program files!
## Once you have copied and pasted each statement, run this statement in your terminal: (replace [REPLACE] with your database credentials)!

export DB_HOST=[REPLACE] (should end in .db.elephantsql.com)
export DB_NAME=[REPLACE]
export DB_USER=[REPLACE] (should be same as DB_NAME)
export DB_PORT=5432
export DB_PASSWORD=[REPLACE]

Note that all of this information can be found in the 'details' section of your instance. DB_HOST is 'Server', DB_NAME and DB_USER is 'User & Default database', and DB_PASSWORD is 'Password'


    CREATE TABLE IF NOT EXISTS gamesRefresh (
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
        correct BOOLEAN
    )


    CREATE TABLE IF NOT EXISTS gamesv3 (
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


    CREATE TABLE IF NOT EXISTS HittingStats (
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



    CREATE TABLE IF NOT EXISTS lineupStats (
        gameId TEXT,
        teamId TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        games_played INTEGER,
        babip TEXT
    )



    CREATE TABLE IF NOT EXISTS PitchingStats (
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




    CREATE TABLE IF NOT EXISTS previousYearHittingStats (
        gameId TEXT,
        teamId TEXT,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        at_bats_per_home_run TEXT,
        games_played INTEGER,
        babip TEXT
    )



    CREATE TABLE IF NOT EXISTS previousYearPitchingStats (
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



    CREATE TABLE IF NOT EXISTS probablesStats (
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




    CREATE TABLE IF NOT EXISTS games (
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





    CREATE TABLE IF NOT EXISTS teamRecords (
        teamName VARCHAR(255),
        numerator INTEGER,
        denominator INTEGER,
        percentage FLOAT,
        insertedYet VARCHAR(255)
    )





    CREATE TABLE IF NOT EXISTS dailyPredictions (
    prediction_date DATE,
    numerator INTEGER,
    denominator INTEGER
  )



    CREATE TABLE IF NOT EXISTS games2022 (
        gameId SERIAL PRIMARY KEY,
        link VARCHAR(255),
        awayTeamId INTEGER,
        homeTeamId INTEGER,
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
        isWinnerHome BOOLEAN
    )


    
    CREATE TABLE IF NOT EXISTS HittingStats2022v3 (
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



    CREATE TABLE IF NOT EXISTS lineupStats2022v3 (
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




    CREATE TABLE IF NOT EXISTS PitchingStats2022v3 (
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



    CREATE TABLE IF NOT EXISTS previousYearHittingStats2022v3 (
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



    CREATE TABLE IF NOT EXISTS previousYearPitchingStats2022V3 (
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



    CREATE TABLE IF NOT EXISTS probablesStats2022V3 (
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


