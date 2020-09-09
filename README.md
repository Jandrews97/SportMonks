# SportMonks
A wrapper for the SportMonks football API. 

# SportMonks Football API 

SportMonks Football API documentation: https://www.sportmonks.com/docs/football/2.0

***NOT YET MADE IT IN TO A PACKAGE***

# Quick Start

Generate an API key from SportMonks: https://sportmonks.com/football-api?soccer
```python
from football import Schedule
schedule = Schedule(api_key)

# returns all fixtures for the current day (JSON format)
fixtures_today = schedule.schedule_today()

# to return in pd.DataFrame format with specified columns (if possible)
fixtures_today = schedule.schedule_today(df=True, df_cols=None)

from football import Odds
odds = Odds(api_key)

# see the best odds offered across bookmakers for a given market 
# use the filters keyword to specify which bookmakers to maximise
# if none given then all bookmakers will be considered

odds.best_odds(fixture_id, market_id, label, filters=None)

# we can also return the average odds

odds.average_odds(fixture_id, market_id, label, filters=None)

from football import Fixtures, FixtureStats

# the Fixtures class allows us to retrieve historical fixtures
# from 2005/2006 onwards by id, date or date range

fixts = Fixtures(api_key)
def by_date_range(start_date: str, end_date: str,
                  team_id: Optional[int] = None,
                  league_ids: Optional[Union[int, List[int]]] = None,
                  markets: Optional[Union[int, List[int]]] = None,
                  bookmakers: Optional[Union[int, List[int]]] = None,
                  includes: Optional[Union[str, List[str]]] = None,
                  filters: Optional[dict] = None,
                  df: bool = False, df_cols: Optional[Union[str, List[str]]] = None)

# see docstrings for more info regarding the arguments

# we can use the relevant includes to harvest statistics from the game
# returns DataFrame of match statistics for home and away team

fixt_stats = FixtureStats(api_key)

# cols keyword is used to specify what columns (stats) you want to keep

fixt_stats.by_date_range(start_date: str, end_date: str,
                         includes: Optional[Union[str, List[str]]] = "stats",
                         filters: Optional[dict] = None,
                         cols: Optional[Union[str, List[str]]] = None)
                         
# we can even return player stats (goals, passes, fouls, cards etc)

fixt_stats.player_by_id(fixture_ids: Union[int, List[int]],
                        includes: Optional[Union[str, List[str]]] = "lineup",
                        filters: Optional[dict] = None,
                        cols: Optional[Union[str, List[str]]] = None):
                        
# one row for each player, so, per fixture, 22 rows

```    
# Database

The file ```run.py``` is run every night to populate new data in to a SQL database
from the fixtures that day. 
This includes all statistics from the fixtures, all player statistics from the fixtures 
and also odds from certain markets.

    
