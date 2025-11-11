SELECT rusher_player_id as "Player Id",
rusher_player_name as "Player Name",
ydstogo as "Yards to Go",
yards_gained as "Yards Gained"
from plays
where rush_attempt = 1;

SELECT ydstogo as "Yards to Go",
avg(yards_gained) as"Average Yards Gained"
from plays
where rush_attempt = 1
group by ydstogo;

SELECT rusher_player_id as "Player Id",
rusher_player_name as "Player Name",
yards_gained as "Yards Gained",
0.12588674 * ydstogo + 3.47336519 as "Expected Yards Gained"
from plays
where rush_attempt = 1;

SELECT rusher_player_id as "Player Id",
rusher_player_name as "Player Name",
yards_gained - (0.12588674 * ydstogo + 3.47336519) as "Yards Over Expected"
from plays
where rush_attempt = 1;

SELECT rusher_player_id as "Player Id",
rusher_player_name as "Player Name",
avg(yards_gained - (0.12588674 * ydstogo + 3.47336519)) as "RYOE",
count(*) as "Rush Attempts"
from plays
where rush_attempt = 1
group by rusher_player_id
having count(*) >= 100
order by "RYOE" desc;