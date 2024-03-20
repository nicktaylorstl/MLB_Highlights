#main.py

import statsapi
import operator
import json
from flask import Flask,render_template,request
from waitress import serve

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        team = form_data['Team']
        player = form_data['Player Name']
        form_year = form_data['Year']
        form_month = form_data['Month']
        form_day = form_data['Day']
        date = f"{form_year}-{form_month}-{form_day}"
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        # return f"{form_data} , {team} , {player}, {year} {month} {day}"

    def get_team_ID(team_name):
        teams = statsapi.lookup_team(team_name)
        for team in teams:
            if team_name.lower() in team['name'].lower():
                return team['id']
            else:
                print('Team not found')
                return 00000
            

    def get_season_schedule(team, year, month=0, day=0):
        team_ID = get_team_ID(team)
        if day ==0 and month ==0:
            schedule = statsapi.schedule(start_date=f"01/01/{year}",end_date=f"12/31/{year}",team= team_ID)
        elif day == 0:
            schedule = statsapi.schedule(start_date=f"{month}/01/{year}",end_date=f"{month}/31/{year}",team= team_ID)
        elif month == 0:
            schedule = statsapi.schedule(start_date=f"01/{day}/{year}",end_date=f"12/{day}/{year}",team= team_ID)
        else: 
            schedule = statsapi.schedule(start_date=f"{month}/{day}/{year}",end_date=f"{month}/{day}/{year}",team= team_ID)
        count = 1
        team_schedule = []
        for game in schedule:
            if game['game_type'] == 'R' and game['away_score'] != game['home_score']:
                #print(f"Game # {count}")
                #print(game['game_id'],game['game_date'],game['away_name'],game['away_score'],game['home_name'],game['home_score'])
                team_schedule.append(game)
                count+=1
        return team_schedule


    def get_player_highlights(player, team, year,month=0,day=0,filter = ' '):
        season_schedule = get_season_schedule(team, year,month,day)
        game_ids = []
        player_highlights = []
        for game in season_schedule:
            game_ids.append(game['game_id'])
        for game_id in game_ids:
            highlights_string = statsapi.game_highlights(game_id)
            highlights_list = highlights_string.split('\n\n')
            for highlight in highlights_list:
                if player.lower() in highlight.lower() and filter.lower() in highlight.lower():
                    highlight = highlight.split('\n')
                    player_highlights.append(highlight)
        return player_highlights

    def get_multiple_player_highlights(players_teams, year,month=0,day=0,filter=' '):
        group_highlights = []
        for player in players_teams:
            player_highlights = get_player_highlights(player, players_teams[player], year,month,day,filter)
            group_highlights.append(player_highlights)
        return group_highlights

    highlights_group = get_player_highlights(player,team,year,month,day)
    highlights = ""
    for highlight_list in highlights_group:
        if len(highlight_list) >= 2:
            title = highlight_list[0]
            description = highlight_list [1]
            url = highlight_list [2]
            highlights += title + "<br>" + description + "<br>" + f"<a href={url} target='_blank'>Watch Video</a>" +"<br>"+"<br>"
        else: 
            title = highlight_list[0]
            description = highlight_list [0]
            url = highlight_list [0]
            highlights += title + "<br>" + description + "<br>" + f"<a href={url} target='_blank'>Watch Video</a>" +"<br>"+"<br>"
    return render_template('data.html', form_data=form_data, highlights=highlights)

    


# nick_fantasy_team = {'Elly de la cruz':'Reds'}
# fantasy_team = get_multiple_player_highlights(nick_fantasy_team, 2023,7,0,'steal')
# for player_highlights in fantasy_team:
#     for highlight in player_highlights:
#         print(highlight+ '\n')

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)