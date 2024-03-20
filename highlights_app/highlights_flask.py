from flask import Flask, render_template, request
import sqlite3
import project_variables as pv
from datetime import datetime, timedelta

season_id = pv.season_id
teams  = {1:"Nick",2:"Phillip",3:"Andrew",4:"Josh",5:"Wesley",6:"Becky",7:"Nate",8:"Paul",9:"Lonnie",10:"Caleb"}
app = Flask(__name__,template_folder='templates')

def yesterday(frmt='%Y-%m-%d', string=True):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday
date = pv.yesterday()
@app.route('/')
def index():

    return render_template('index.html',date=date,yesterday=yesterday)

@app.route('/team/<team_id>/<date>')
def team_page(team_id,date=None):
    if date is None:
        date = pv.yesterday()

    # Connect to the SQLite database
    conn = sqlite3.connect('data/MLB_Highlights.db')
    cursor = conn.cursor()
    team_owner = teams[int(team_id)]
    # Execute SQL query
    cursor.execute(f"""
                    SELECT player_name,date,headline,description,mp4_url,yahoo_team_name,mlb_team_name
                    FROM yahoo_highlights_{season_id}
                    Where team_id = {team_id} and date = '{date}'
                    ORDER BY player_name, date
                    """
                    )
    highlights = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Render the template with the query results
    return render_template('teams.html', highlights=highlights, date=date,team_owner=team_owner)

if __name__ == '__main__':
    app.run(debug=True)
