import sqlite3
import pandas as pd
import project_variables as pv

season_id = pv.season_id
database_filepath = pv.database_filepath
def update_sqlite():
    game_data_df = pd.read_csv(f'data/game_data_{season_id}.csv')
    highlights_df = pd.read_csv(f'data/highlights_{season_id}.csv')
    rosters_df = pd.read_csv(f'data/yahoo_rosters_{season_id}.csv')

    conn = sqlite3.connect(database_filepath)
    game_data_df.to_sql(f'game_data_{season_id}', conn, if_exists='replace')
    highlights_df.to_sql(f'highlights_{season_id}', conn, if_exists='replace')
    rosters_df.to_sql(f'yahoo_rosters_{season_id}', conn, if_exists='replace')
    conn.close()
    print(f"{database_filepath} was updated")

def update_final_table():
    conn = sqlite3.connect(database_filepath)
    cur = conn.cursor()
    res = cur.execute(f"""
                    with source as 
                        (select g.game_id, g.date, g.away_name, g.home_name, h.player_name, h.headline, h.description, h.mp4_url 
                        from highlights_2024_pre as h
                        LEFT join game_data_{season_id} as g on g.game_id = h.game_id)

                    select s.*, y.team_id, y.team_name as yahoo_team_name, y.mlb_team_name,y.primary_position
                    from source as s
                    left join yahoo_rosters_{season_id} as y on s.player_name = y.player_name and s.date =y.date
                    """)
    data = res.fetchall()
    cur.close()

    cur=conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS yahoo_highlights_{season_id}")
    cur.execute(f"""
                CREATE TABLE IF NOT EXISTS yahoo_highlights_{season_id} (
            game_id INTEGER,
            date DATE,
            away_name STRING,
            home_name STRING,
            player_name STRING,
            headline STRING,
            description STRING,
            mp4_url STRING,
            team_id INTEGER,
            yahoo_team_name STRING,
            mlb_team_name STRING,
            primary_position STRING
        )
    """)

    cur.executemany(f"INSERT INTO yahoo_highlights_{season_id} VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",data)
    print(f"yahoo_highlights_{season_id} was updated")
    conn.commit()
    conn.close()
