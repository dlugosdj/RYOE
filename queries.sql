SELECT rusher_player_id as "Player Id", rusher_player_name as "Player Name", ydstogo as "Yards to Go", yards_gained as "Yards Gained"
from plays
where rush_attempt = 1;

SELECT ydstogo as "Yards to Go", avg(yards_gained) as"Average Yards Gained"
from plays
where rush_attempt = 1
group by ydstogo;
