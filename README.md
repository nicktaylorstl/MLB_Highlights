# MLB_Highlights
This is a program that creates an SQLite database with daily highlight info from MLB Stats API, as well as daily roster info from my fantasy baseball league using Yahoo Fantasy API

It gets the basic data for each game, and the specific information for each highlight video.
Then it merges this with the daily roster information and copies the database to another folder for use in the Cool WHIPS Highlights repository, which creates a webapp from the database
https://github.com/nicktaylorstl/CoolWHIPHighlights

 
To get the yahoo fantasy data I used code from this repository by Edward Distel
 https://github.com/edwarddistel/yahoo-fantasy-baseball-reader 
