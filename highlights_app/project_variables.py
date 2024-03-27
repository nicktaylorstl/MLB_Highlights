from google.oauth2 import service_account
import json
full_path = "D:/Documents/GFA/SportsPython/Baseball/MLB_Highlights/"
season_id = '2024'
yahoo_rosters_filepath = f"{full_path}data/yahoo_rosters_{season_id}.csv"
highlights_filepath = f"{full_path}data/highlights_{season_id}.csv"
game_data_filepath = f"{full_path}data/game_data_{season_id}.csv"
roster_full_data_filepath = f"{full_path}data/yahoo_rosters_full_data_{season_id}.csv"
bigquery_table_id = season_id


from datetime import datetime, timedelta

credentials = service_account.Credentials.from_service_account_file(
    f"{full_path}secrets/google_key.json"
)

database_filepath = f'{full_path}data/MLB_Highlights.db'
website_database = 'D:/Documents/GFA/SportsPython/Baseball/CoolWHIPHighlights/MLB_Highlights.db'

def yesterday(frmt='%Y-%m-%d', string=True):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday