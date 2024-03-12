with source as 
    (select g.game_id, g.date, g.away_name, g.home_name, h.player_name, h.headline, h.description, h.mp4_url 
    from `mlbhighlights`.`highlights`.`2024_pre` as h
    LEFT join `mlbhighlights`.`games`.`2024_pre` as g on g.game_id = h.game_id)

select s.*, y.team_id, y.team_name as yahoo_team_name, y.mlb_team_name,y.primary_position
from source as s
left join `mlbhighlights`.`yahoo_rosters`.`2024_pre` as y on s.player_name = y.player_name and s.date =y.date