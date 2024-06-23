<h1 align="center">MLB GAME PREDICTOR</h1>

<p align="center">
  <a href="http://www.mlbgamepredictor.com">www.mlbgamepredictor.com</a>
</p>

<p align="center">
  <img width="1436" alt="Home Page" src="https://github.com/Michael-Goldfarb/MLBGamePredictor/assets/66848094/6fc0e768-42aa-4260-a544-fced9de8fbe0">
  <br>
  <em>Home Page with information from each matchup of the day, including updated scores, game time, game status, and the prediction of the winner of the game. If the prediction was right, the prediction will be in green text. If the prediction was wrong, the prediction will be in red text.</em>
</p>

<p align="center">
  <img width="1440" alt="Screenshot 2023-07-25 at 8 18 30 AM" src="https://github.com/Michael-Goldfarb/MLBGamePredictor/assets/66848094/77f9030b-d096-4920-bf75-7fd01e78f317">
  <br>
  <em>History page with daily prediction records and overall prediction record. There is also a spot to see the overall prediction record by team, to be able to tell which teams the model is best and worst at predicting. I added buttons to sort by the teams the model is best at predicting, and the teams the model is worst at predicting.</em>
</p>

<p align="center">
  <img width="1440" alt="Screenshot 2023-07-25 at 8 19 41 AM" src="https://github.com/Michael-Goldfarb/MLBGamePredictor/assets/66848094/72afeb2e-2fcc-492e-b70d-9c43bf63da53">
  <br>
  <em>This is the page the user is sent to after logging in with Google. They have the option to either be sent to the predictions page, or log out. I implemented Google OAuth for Google Sign In.</em>
</p>

## How to Use:
1. Open a terminal and paste the below text:
2.     git clone https://github.com/Michael-Goldfarb/MLBGamePredictor.git
3. Open up three terminals and cd into MLBGamePredictor by typing 'cd MLBGamePredictor' in each terminal
4. In one terminal, run 'git checkout backend'
5. In the same terminal, run 'cd tables', then 'cd currentTables'
6. Follow the instructions on the Notes.md file
7. In /currentTables, run the following files:
8.     python todaysgames.py
9.     python gamesv3.py
10.     python gamesrefresh.py
11.     python hittingstats.py
12.     python pitchingstats.py
13.     python probablesstats.py
14.     python lineupstats.py
15.     python previousyearhittingstats.py
16.     python previousyearpitchingstats.py
17. Then, in another terminal, run 'cd tables'
18. In that terminal, run the following files:
19.     python prediction1.py
20.     python prediction2.py
21.     python prediction3.py
22.     python prediction4.py
23.     python prediction5.py
24. Then, to start the website, in the same terminal, run 'cd ..', then 'cd backend', then 'mvn spring-boot:run'
25. Open up your third terminal, run 'git checkout web', then 'cd web', then 'cd web', then 'npm start'
26. Now the website is started! For more up-to-date predictions and game scores, run the gamesRefresh file, the prediction5.py file, and run the lineupStats.py and previousyearhittingstats tables, because lineups are only put out a few hours before the start of the game and could change.
