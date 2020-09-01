"""
Run every night to insert the new information from fixtures that day
in to PostgreSQL database.
"""
import time
from datetime import datetime
import db_cols
from to_database import fixtures_data_to_sql, to_psql, ENGINE
from football import Continents, Countries, Bookmakers, Markets, Leagues, Seasons

start_time = time.time()
today = datetime.today().strftime('%Y-%m-%d')

if __name__ == "__main__":

    with ENGINE.begin() as con:

        to_psql(Continents().continents(), table="Continents", engine=con,
                if_exists="replace", cols=["id", "name"])

        to_psql(Countries().countries(), table="Countries", engine=con,
                if_exists="replace", cols=["id", "name"])

        to_psql(Bookmakers().bookmakers(), table="Bookmakers", engine=con,
                if_exists="replace", cols=["id", "name"])

        to_psql(Markets().markets(), table="Markets", engine=con,
                if_exists="replace", cols=["id", "name"])

        to_psql(Leagues().by_id(), table="Leagues", engine=con,
                if_exists="replace", cols=["id", "name"])

        to_psql(Seasons().seasons(), table="Seasons", engine=con,
                if_exists="replace", cols=["id", "name", "league_id"])


    for league in db_cols.LEAGUES:

        fixtures_data_to_sql(today, today, league_ids=db_cols.LEAGUES[league],
                             table=league, if_exists="append", engine=ENGINE,
                             markets=[1, 12, 976105, 976334,
                                      976316, 136703818, 136830811],
                             bookmakers=[2, 9, 15, 187, 27802, 271057011, 271057013],
                             includes="league.country,localTeam,visitorTeam,\
                                       localCoach,visitorCoach,\
                                       venue,referee,stats,lineup,odds",
                             cols=db_cols.FIXTURE_COLUMNS,
                             cols_rename=db_cols.RENAME_FIXT_COLUMNS)

print(f"---Time elapsed: {time.time() - start_time} seconds---")
