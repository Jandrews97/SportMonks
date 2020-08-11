"""
Script that runs every night to populate PostgreSQL database
with information form the SportMonks API

"""
import time
from datetime import datetime
import columns
import PSQL as psql
import sportmonks as sm

start_time = time.time()
today = datetime.today().strftime('%Y-%m-%d')

if __name__ == "__main__":
    psql.to_psql(sm.get_continents(), table="Continents", engine=psql.ENGINE,
                 if_exists="replace", cols=["id", "name"])

    psql.to_psql(sm.get_countries(), table="Countries", engine=psql.ENGINE,
                 if_exists="replace", cols=["id", "name"])

    psql.to_psql(sm.get_bookmakers(), table="Bookmakers", engine=psql.ENGINE,
                 if_exists="replace", cols=["id", "name"])

    psql.to_psql(sm.get_markets(), table="Markets", engine=psql.ENGINE,
                 if_exists="replace", cols=["id", "name"])

    psql.to_psql(sm.get_leagues(), table="Leagues", engine=psql.ENGINE,
                 if_exists="replace", cols=["id", "name"])

    psql.to_psql(sm.get_seasons(), table="Seasons", engine=psql.ENGINE,
                 if_exists="'replace", cols=["id", "name", "league_id"])

    for league in columns.LEAGUES:

        psql.fixtures_data_to_sql(today, today, league_ids=columns.LEAGUES[league],
                                  table=league, if_exists="append", engine=psql.ENGINE,
                                  markets=[1, 12, 976105, 976334,
                                           976316, 976105, 136703818, 136830811],
                                  bookmakers=[2, 9, 15, 187, 27802, 271057011, 271057013],
                                  includes="league.country,localTeam,visitorTeam,\
                                            localCoach,visitorCoach,\
                                            venue,referee,stats,lineup,odds",
                                  cols=columns.FIXTURE_COLUMNS,
                                  cols_rename=columns.RENAME_FIXT_COLUMNS)


    print(f"---Time elapsed: {time.time() - start_time} seconds---")
