import rosters_update as r
import highlights_update as h
import sqlite_update as sq
import project_variables as pv

pull_date = pv.yesterday()

csv_game_ids = h.get_game_Ids(pull_date)
for game in csv_game_ids:
    if h.is_game_id_present(game):
        print(f"Game ID {game} was already inserted")
        continue
    
    h.game_insert(game)

r.update_yahoo_roster(pull_date)
sq.update_sqlite() 
sq.update_final_table()
sq.copy_database()