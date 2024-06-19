import rosters_update as r
import highlights_update as h
import sqlite_update as sq
import project_variables as pv

#pull_date = pv.yesterday()

pull_dates = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18"]

for date in pull_dates:

    pull_date = f"2024-06-{date}"
    csv_game_ids = h.get_game_Ids(pull_date)

    print('Updating Game Highlight Data')
    print()
    for game in csv_game_ids:
        h.game_insert(game)
    print('------------------------------------------------------------------------')

    print('Updating Daily Yahoo Roster')
    print()
    r.update_yahoo_roster(pull_date)
    print('------------------------------------------------------------------------')

    print('Updating FULL DATA Yahoo Roster')
    print()
    r.full_data_roster_append()
    print('------------------------------------------------------------------------')

    print("Updating Database")
    print()
    sq.update_sqlite() 
    sq.update_final_table()
    sq.copy_database()
    print(pull_date)
