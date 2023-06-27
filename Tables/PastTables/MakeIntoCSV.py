import requests
import json
from datetime import datetime
import csv

response = requests.get("http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-06-07&endDate=2022-08-07")
data = response.json()
lineup = []
teamsLineup = []
dates = []
gamesId = []
outcomes = []
i = 0
for date_info in data["dates"]:
    for game in date_info["games"]:
        gameId = game['gamePk']
        for _ in range(18):
            gamesId.append(gameId)
        gameDate = game['officialDate']
        print(gameDate)
        awayTeamId = game['teams']['away']['team']['id']
        homeTeamId = game['teams']['home']['team']['id']
        awayTeamName = game['teams']['away']['team']['name']
        homeTeamName = game['teams']['home']['team']['name']
        isWinnerAway = game['teams']['away'].get('isWinner')
        if isWinnerAway is not None:
            for _ in range(9):
                outcomes.append(isWinnerAway)
        else:
            for _ in range(9):
                outcomes.append(False)
        isWinnerHome = game['teams']['home'].get('isWinner')
        if isWinnerHome is not None:
            for _ in range(9):
                outcomes.append(isWinnerHome)
        else:
            for _ in range(9):
                outcomes.append(False)
        if i == 0: # uses the first game twice for some reason
            i += 1
            continue
        if gameId == 663466: # all star game
            continue
        url = f"https://statsapi.mlb.com/api/v1.1/game/{game['gamePk']}/feed/live"
        response = requests.get(url)
        data = response.json()

        awayTeamName = data['gameData']['teams']['away']['name']
        homeTeamName = data['gameData']['teams']['home']['name']
        # Parse battingOrder if it is a string representation of an array
        battingOrderHome_str = data['liveData']['boxscore']['teams']['home'].get('battingOrder')
        if isinstance(battingOrderHome_str, str):
            battingOrderHome = json.loads(battingOrderHome_str)
        else:
            battingOrderHome = battingOrderHome_str

        battingOrderAway_str = data['liveData']['boxscore']['teams']['away'].get('battingOrder')
        if isinstance(battingOrderAway_str, str):
            battingOrderAway = json.loads(battingOrderAway_str)
        else:
            battingOrderAway = battingOrderAway_str

        if len(battingOrderAway) >= 9:
            for _ in range(9):
                dates.append(gameDate)
            batterOneAway = battingOrderAway[0]
            lineup.append(battingOrderAway[0])
            teamsLineup.append(awayTeamName)
            batterTwoAway = battingOrderAway[1]
            lineup.append(battingOrderAway[1])
            teamsLineup.append(awayTeamName)
            batterThreeAway = battingOrderAway[2]
            lineup.append(battingOrderAway[2])
            teamsLineup.append(awayTeamName)
            batterFourAway = battingOrderAway[3]
            lineup.append(battingOrderAway[3])
            teamsLineup.append(awayTeamName)
            batterFiveAway = battingOrderAway[4]
            lineup.append(battingOrderAway[4])
            teamsLineup.append(awayTeamName)
            batterSixAway = battingOrderAway[5]
            lineup.append(battingOrderAway[5])
            teamsLineup.append(awayTeamName)
            batterSevenAway = battingOrderAway[6]
            lineup.append(battingOrderAway[6])
            teamsLineup.append(awayTeamName)
            batterEightAway = battingOrderAway[7]
            lineup.append(battingOrderAway[7])
            teamsLineup.append(awayTeamName)
            batterNineAway = battingOrderAway[8]
            lineup.append(battingOrderAway[8])
            teamsLineup.append(awayTeamName)

        if len(battingOrderHome) >= 9:
            for _ in range(9):
                dates.append(gameDate)
            batterOneHome = battingOrderHome[0]
            lineup.append(battingOrderHome[0])
            teamsLineup.append(homeTeamName)
            batterTwoHome = battingOrderHome[1]
            lineup.append(battingOrderHome[1])
            teamsLineup.append(homeTeamName)
            batterThreeHome = battingOrderHome[2]
            lineup.append(battingOrderHome[2])
            teamsLineup.append(homeTeamName)
            batterFourHome = battingOrderHome[3]
            lineup.append(battingOrderHome[3])
            teamsLineup.append(homeTeamName)
            batterFiveHome = battingOrderHome[4]
            lineup.append(battingOrderHome[4])
            teamsLineup.append(homeTeamName)
            batterSixHome = battingOrderHome[5]
            lineup.append(battingOrderHome[5])
            teamsLineup.append(homeTeamName)
            batterSevenHome = battingOrderHome[6]
            lineup.append(battingOrderHome[6])
            teamsLineup.append(homeTeamName)
            batterEightHome = battingOrderHome[7]
            lineup.append(battingOrderHome[7])
            teamsLineup.append(homeTeamName)
            batterNineHome = battingOrderHome[8]
            lineup.append(battingOrderHome[8])
            teamsLineup.append(homeTeamName)

    # Create the CSV file and write the data
    with open('lineup_stats.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['gameID', 'theDate', 'player_id', 'player_name', 'obp', 'slg', 'ops', 'at_bats_per_home_run', 'team_name', 'games_played', 'babip', 'isWinner'])

        # Loop through each player in the lineup
        for index, player_id in enumerate(lineup):
            team_name = teamsLineup[index]  # Get the team name corresponding to the current player
            newGameId = gamesId[index]
            isWinner = outcomes[index]
            theDate = dates[index]

            try:
                # Make the API request to fetch player stats
                api_url = "https://statsapi.mlb.com/api/v1/people/{playerId}/stats?stats=byDateRange&season=2022&group=hitting&startDate=04/07/2022&endDate={currentDate}&leagueListId=mlb_milb".format(
                    playerId=player_id,
                    currentDate=theDate
                )
                response = requests.get(api_url)
                data = response.json()

                # Extract the required fields
                stats = data["stats"][0]["splits"][0]["stat"]
                api_url2 = "https://statsapi.mlb.com/api/v1/people/{playerId2}".format(
                    playerId2=player_id,
                )
                response2 = requests.get(api_url2)
                data2 = response2.json()
                player_name = data2["people"][0]["fullName"]
                games_played = stats["gamesPlayed"]
                obp = stats["obp"]
                slg = stats["slg"]
                ops = stats["ops"]
                at_bats_per_home_run = stats["atBatsPerHomeRun"]
                babip = stats["babip"]
                print(babip)

                # Write the player stats to the CSV file
                writer.writerow([newGameId, theDate, player_id, player_name, obp, slg, ops, at_bats_per_home_run, team_name, games_played, babip, isWinner])

            except IndexError:
                print("Player stats not available for player ID:", player_id)
                
print("Data saved to lineup_stats.csv")
