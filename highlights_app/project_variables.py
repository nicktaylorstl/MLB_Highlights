from google.oauth2 import service_account
import json

season_id = '2024_pre'
yahoo_rosters_filepath = f"data/yahoo_rosters_{season_id}.csv"
highlights_filepath = f"data/highlights_{season_id}.csv"
game_data_filepath = f"data/game_data_{season_id}.csv"
bigquery_table_id = season_id
from datetime import datetime, timedelta

credentials = service_account.Credentials.from_service_account_file(
    'secrets/google_key.json'
)

database_filepath = 'data/MLB_Highlights.db'

def yesterday(frmt='%Y-%m-%d', string=True):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday