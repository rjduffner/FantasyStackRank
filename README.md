FantasyStackRank
================




Sample Queries

Get Standings Data: select * from fantasysports.leagues.standings where league_key='%s'

Get Team Statistics: select * from fantasysports.teams.stats where team_key='%s'

Get Stat Id's: select * from fantasysports.leagues.settings where league_key='341.l.13222'

Get Week By Week: select * from fantasysports.leagues.scoreboard where league_key='341.l.13222' and week=1
