
import csv
from datetime import datetime, timedelta
import unidecode
from google.cloud import bigquery
from google.oauth2 import service_account
import re
import project_variables as pv

season_id = pv.season_id
yahoo_rosters_filepath = pv.yahoo_rosters_filepath
highlights_filepath = pv.highlights_filepath
game_data_filepath = pv.game_data_filepath
bigquery_table_id = season_id

credentials = pv.credentials

client = bigquery.Client(credentials=credentials)

time_of_insertion = datetime.now()
inserted = time_of_insertion.strftime('%Y-%m-%d %H:%M:%S')


def yahoo_roster_to_bigquery(roster_update):
    
    dataset_id = 'yahoo_rosters'
    table_id = bigquery_table_id

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Insert data into BigQuery table
    errors = client.insert_rows(table, roster_update)

    if not errors:
        print('Data inserted successfully.')
    else:
        print('Errors occurred during data insertion:', errors)

def update_yahoo_roster(date):
    

    
    def remove_parentheses(input_string):
        pattern = r'\s*\([^)]*\)'
        result = re.sub(pattern, '', input_string)
        
        return result

    def roster_to_csv(roster_update, filepath):
        with open(filepath, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                # Check if the combination of date and player name already exists
                if row[0] == roster_update[0] and row[4] == roster_update[4]:
                    print("Duplicate entry found, skipping...")
                    return
        
        with open(filepath, 'a', newline='',encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(roster_update)
            yahoo_roster_to_bigquery([roster_update])

    teams = {}

    with open('data/teams.csv', newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            teams[int(row['team_id'])] = {"name": row["name"], "roster":[]}

    with open('data/rosters.csv', newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = date
            team_id = int(row['team_code'][14:])
            team_name = unidecode.unidecode(teams[team_id]["name"])
            mlb_team_name = row['editorial_team_full_name']
            full_name = unidecode.unidecode(row['full_name'])
            player_name = remove_parentheses(full_name)
            primary_position = row['primary_position']
            teams[team_id]["roster"].append(full_name)
            time_of_insertion = datetime.now()
            inserted = time_of_insertion.strftime('%Y-%m-%d %H:%M:%S')
            roster_update = date,team_id,team_name,mlb_team_name,player_name,primary_position,inserted
        
            roster_to_csv(roster_update,yahoo_rosters_filepath)
            print(roster_update)
            
