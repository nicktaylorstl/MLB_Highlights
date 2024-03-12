# MLB_Highlights
This is my first attempt at creating a flask web app. 

I used the free MLB stats API to get links to player highlight videos.

With the webapp you can select a player name and a specific date or a full month and it will return links to all of the highlight videos of that player from the specified time. 

You can access it here https://mlb-highlights.onrender.com/

If you want to see two great catches, search for Tommy Edman - St. Louis Cardinals - 2023 June 29

I am currently working on adding the data to a separate database (currently using BigQuery) so that the website can query my own database instead of calling the API each time. This will make website queries faster and also allow more freedom in the types of queries I can create. 

Currently it's set up with daily_highlights.py calling the MLB_Stats api and putting the highlights from the previous day into BigQuery and also two csv files game_data_2024_pre.csv and highlights_2024_pre.csv 

daily_highlights.py now includes functions to retrieve the roster information from our fantasy baseball league using Yahoo Sports API, and add this to a table in Big Query, so that we can query the highlights based on which fantasy baseball team a player is on. 
