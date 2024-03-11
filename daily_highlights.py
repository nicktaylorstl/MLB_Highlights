import statsapi
import operator
import json
import csv
from datetime import datetime, timedelta
import unidecode
from google.cloud import bigquery
from google.oauth2 import service_account

highlights_filepath = "data/highlights_2024_pre.csv"
game_data_filepath = "data/game_data_2024_pre.csv"
bigquery_table_id = '2024_pre'

time_of_insertion = datetime.now()
inserted = time_of_insertion.strftime('%Y-%m-%d %H:%M:%S')

# sample game_id = 718437
#write single highlight to csv
def highlight_to_csv(highlight_str, filepath):
    with open(filepath, 'a', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(highlight_str)

# write game data from one game to a csv
def game_data_insert(game_id):
    boxscore = statsapi.boxscore_data(game_id)
    date = boxscore["gameId"][:10]
    date = date.replace('/','-')
    year = int(date[:4])

    away_name = boxscore["teamInfo"]["away"]["teamName"]
    away_id = boxscore["teamInfo"]["away"]["id"]
    home_name = boxscore["teamInfo"]["home"]["teamName"]
    home_id = boxscore["teamInfo"]["home"]["id"]
    away_score = boxscore["away"]["teamStats"]["batting"]["runs"]
    home_score= boxscore["home"]["teamStats"]["batting"]["runs"]

    game_data = [game_id,date,away_name,away_id,away_score,home_name,home_id,home_score,inserted]


    with open(game_data_filepath, 'a', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(game_data)
    game_data_to_bigquery([game_data])

# write all the highlights from one game to a csv
def game_highlights_insert(game_id):
    data = statsapi.game_highlight_data(game_id)
    highlights = statsapi.game_highlight_data(game_id)

    # Write data to the CSV file
    for highlight in highlights:
        headline = unidecode.unidecode(highlight["headline"])
        date = highlight["date"]
        year = int(date[:4])
        if 'blurb' not in highlight and 'description' not in highlight:
            blurb = "no blurb available"
            description = "no description available"
        else:
            if 'blurb' in highlight:
                blurb = unidecode.unidecode(highlight["blurb"])
            else: blurb = unidecode.unidecode(highlight["description"])
            if 'description' in highlight:
                description = unidecode.unidecode(highlight["description"])
            else: description = blurb
        mp4_url = highlight["playbacks"][0]["url"]
        duration = highlight["duration"]
        
        has_player = any(item['type'] == 'player_id' for item in highlight['keywordsAll'])
        if has_player:
            player_info = [(item['value'], item['displayName']) for item in highlight['keywordsAll'] if item['type'] == 'player_id']
        else:
            player_info = [(0, 'NA')]
        player_id = player_info[0][0]
        player_name = unidecode.unidecode(player_info[0][1])


        highlight_list = [game_id,date,player_name,player_id,headline,blurb,description,mp4_url,duration,inserted]
    
        highlight_to_csv(highlight_list,highlights_filepath)
        highlight_to_bigquery([highlight_list])


def yesterday(frmt='%Y-%m-%d', string=True):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday

def get_game_Ids(date):
    schedule = statsapi.schedule(date)
    game_ids = []
    for game in schedule:
        game_ids.append(game['game_id'])
    return game_ids





# WRITING THE DATA TO BIG QUERY

credentials = service_account.Credentials.from_service_account_file(
    'secrets/google_key.json'
)
client = bigquery.Client(credentials=credentials)

def highlight_to_bigquery(highlight):
    dataset_id = 'highlights'
    table_id = bigquery_table_id

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)
    

    # Insert data into BigQuery table
    errors = client.insert_rows(table, highlight)

    if not errors:
        print('Data inserted successfully.')
    else:
        print('Errors occurred during data insertion:', errors)

def game_data_to_bigquery(gamedata):
    dataset_id = 'games'
    table_id = bigquery_table_id

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Insert data into BigQuery table
    errors = client.insert_rows(table, gamedata)

    if not errors:
        print('Data inserted successfully.')
    else:
        print('Errors occurred during data insertion:', errors)


def is_game_id_present(new_game_id):

    with open(game_data_filepath, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) #This skips the header row

        for row in csv_reader:
            game_id = int(row[0])
            if new_game_id == game_id:
                return True
    return False

def game_insert(game_id):
    game_data_insert(game_id)
    game_highlights_insert(game_id)


dates = ['2024-02-23','2024-02-24','2024-02-25','2024-02-26','2024-02-27','2024-02-28','2024-02-29','2024-03-01','2024-03-02','2024-03-03','2024-03-04','2024-03-05']

pull_date = yesterday()

csv_game_ids = get_game_Ids(pull_date)
for game in csv_game_ids:
    if is_game_id_present(game):
        print(f"Game ID {game} was already inserted")
        continue
    game_insert(game)