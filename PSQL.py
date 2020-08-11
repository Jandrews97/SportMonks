"""
Store data from Sportmonks API in PostgreSQL database
"""
import os
import logging
from typing import Dict, Optional, Union, List, Any
import inspect
import copy
import numpy as np
import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import inspect
import enchant
import helper
import sportmonks as sm
import columns

log = helper.setup_logger(__name__, "SM_API.log")
sql_log = helper.setup_logger("sqlalchemy", "sqlalchemy.engine")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

def postgres_engine(driver: str, username: str, password: str,
                    host: str, port: int, database: str):

    """
    Sets up connection to PostgreSQL database.

    Args:
        driver:
            Usually psycopg2 or pg80000.
        username:
            username for the database.
        password:
            password for the database.
        host:
            database host.
        port:
            database port.
        database:
            database name.

    Returns:
        Engine object.
    """

    return create_engine(f"postgresql+{driver}://{username}:{password} \
                         @{host}:{port}/{database}")

ENGINE = postgres_engine("psycopg2", "postgres", POSTGRES_PASSWORD,
                         "localhost", 5432, "SportMonks")
INSPECTOR = inspect(ENGINE)

def to_psql(response: Union[Dict, List[Dict], pd.DataFrame], table: str, engine,
            if_exists: str = "fail", cols: Optional[List[str]] = None,
            chunksize: int = 100000):
    """
    Stores data from SportMonks API in a PostgreSQL database.

    Args:
        response:
            Data from SportMonks API.
        table:
            Name of the table you want to store the data in.
        engine:
            sqlalchemy.engine.base.Engine type; connection to database.
        if_exists: default = "fail"
            what to do if the table already exists,
            must be "fail", "replace" or "append".
        cols: optional
            What columns you want in your table.
        chunksize: default = 100000
            Specify the number of rows in each batch to be written at a time.
            By default, all rows will be written at once.

    Returns:
        None

    """

    log.info("Creating Table: %s", table)
    assert if_exists in ("fail", "replace", "append"), \
        "if exists must be; \"fail\", \"replace\" or \"append\""

    if isinstance(response, pd.DataFrame):
        if cols:
            try:
                response[cols].to_sql(table, con=engine, index=False,
                                      if_exists=if_exists, chunksize=chunksize)
            except KeyError as e:
                raise KeyError(f"The column is not in the API response: {e}")
            except sqlalchemy.exc.DBAPIError as e:
                if e.orig.pgcode == '42703':
                    print(f"Column exception: {e.orig.diag.message_primary}")
                    data = pd.read_sql(f"SELECT * FROM public.\"{table}\"", con=engine)
                    new_response = pd.concat([data, response[cols]])
                    new_response.to_sql(table, con=engine, index=False,
                                        if_exists="replace", chunksize=chunksize)
                else:
                    print(f"Error: {e.orig.diag.message_primary}")
                    raise
        else:
            try:
                response.to_sql(table, con=engine, index=False,
                                if_exists=if_exists, chunksize=chunksize)
            except sqlalchemy.exc.DBAPIError as e:
                if e.orig.pgcode == '42703':
                    print(f"Column exception: {e.orig.diag.message_primary}")
                    data = pd.read_sql(f"SELECT * FROM public.\"{table}\"", con=engine)
                    new_response = pd.concat([data, response])
                    new_response.to_sql(table, con=engine, index=False,
                                        if_exists="replace", chunksize=chunksize)
                else:
                    print(f"Error: {e.orig.diag.message_primary}")
                    raise
    else:
        if cols:
            try:
                pd.json_normalize(response)[cols].to_sql\
                (table, con=engine, index=False,
                 if_exists=if_exists, chunksize=chunksize)
            except KeyError as e:
                raise KeyError(f"The column is not in the API response: {e}")
            except sqlalchemy.exc.DBAPIError as e:
                print(f"Column exception: {e.orig.diag.message_primary}")
                if e.orig.pgcode == '42703':
                    data = pd.read_sql(f"SELECT * FROM public.\"{table}\"", con=engine)
                    new_response = pd.concat([data, pd.json_normalize(response)[cols]])
                    new_response.to_sql(table, con=engine, index=False,
                                        if_exists="replace", chunksize=chunksize)
                else:
                    print(f"Error: {e.orig.diag.message_primary}")
                    raise
        else:
            try:
                pd.json_normalize(response).to_sql(table, con=engine,
                                                   index=False, if_exists=if_exists,
                                                   chunksize=chunksize)
            except sqlalchemy.exc.DBAPIError as e:
                if e.orig.pgcode == '42703':
                    print(f"Column exception: {e.orig.diag.message_primary}")
                    data = pd.read_sql(f"SELECT * FROM public.\"{table}\"", con=engine)
                    new_response = pd.concat([data, pd.json_normalize(response)])
                    new_response.to_sql(table, con=engine, index=False,
                                        if_exists="replace", chunksize=chunksize)
                else:
                    print(f"Error: {e.orig.diag.message_primary}")
                    raise

    log.info("%s", INSPECTOR.get_table_names())

    return None

def stats_includes(response: Union[Dict, List[Dict]]):

    """
    Prepares the stats includes from the fixures endpoint
    for json_normalize.
    ***Must use the stats includes.

    Args:
        response:
            Response from SportMonks API; JSON format.

    Returns:
        Transformed response, ready for use of json_normalize
    """

    if isinstance(response, list):
        for fixt in response:
            statistics = fixt.get("stats")
            if len(statistics) == 2:
                fixt["home"] = statistics[0]
                fixt["away"] = statistics[1]
                del fixt["stats"]
            else:
                log.info("Length of statistics: %s", len(statistics))
                fixt["home"] = {}
                fixt["away"] = {}
                del fixt["stats"]

    elif isinstance(response, dict):
        statistics = response.get("stats")
        if len(statistics) == 2:
            response["home"] = statistics[0]
            response["away"] = statistics[1]
            del response["stats"]
        else:
            log.info("Length of statistics: %s", len(statistics))
            response["home"] = {}
            response["away"] = {}
            del response["stats"]

    return response

def odds_includes(response: Union[Dict, List[Dict]], markets: Union[int, List[int]],
                  table: str, if_exists: str, engine):
    """
    For each fixture, populates SQL table(s) with odds information
    from the fixtures endpoint.
    ***Must use the odds includes.

    Args:
        response:
            Response from SportMonks API; JSON format.
        markets:
            The markets you want to create tables for.
        table:
            Name of SQL table.
        if_exists:
            What to do if the table already exists,
            must be "fail", "replace" or "append".
        engine:
            sqlalchemy.engine.base.Engine type; connection to database.

    Returns:
        None

    """
    odds_list = [[] for _ in range(len(markets))]
    for p, i in enumerate(markets):
        odds_list[p].append(i)

    to_process = response if isinstance(response, list) else [response]

    for fixt in to_process:
        if fixt.get("odds") == []:
            log.info("No odds included")
            continue
        odds = fixt.get("odds")
        log.info("Number of markets: %s", len(odds))

        for market in odds:
            fixture_odds_dict = {"id": fixt.get("id")}
            fixture_odds_dict["market_id"] = market.get("id")
            fixture_odds_dict["market"] = market.get("name")
            bookmaker = market.get("bookmaker")

            for i in bookmaker:
                log.info("Number of bookmakers: %s", len(bookmaker))
                actual_odds = i.get("odds")
                log.info("Actual odds: %s", len(actual_odds))
                home = fixt.get("localTeam").get("name")
                home_short = fixt.get("localTeam").get("short_code")
                away = fixt.get("visitorTeam").get("name")
                away_short = fixt.get("visitorTeam").get("short_code")
                actual_odds = standardise_columns(actual_odds, home, away,
                                                  home_short, away_short)
                if market.get("id") == 976105:
                    labels = [j.get("label") for j in actual_odds]
                    if any(n not in ["Yes", "No"] for n in labels):
                        log.debug("Incorrect label for BTTS: %s", labels)
                        continue

                for j in actual_odds:
                    if market.get("id") == 12:
                        if j.get("label") not in ["Over", "Under"]:
                            log.info("Incorrect Over/Under label: %s",
                                     j.get("label"))
                            continue
                    if market.get("id") == 976316:
                        if all(x not in j.get("label") for x in ["Yes", "No"]) or \
                           all(x not in j.get("label") for x in ["1", "X", "2"]):
                            log.debug("Incorrect label for Result/BTTS: %s",
                                      j.get("label"))
                            continue

                    if j.get("total") is not None:
                        if ("." in j.get("total")) and (j.get("total").split(".")[1] == "5"):
                            fixture_odds_dict[
                                i.get("name")+"_"+j.get("label")+str(j.get("total"))
                                ] = j.get("value")
                    else:
                        fixture_odds_dict[
                            i.get("name")+"_"+j.get("label")
                            ] = j.get("value")

            for z in odds_list:
                if z[0] == fixture_odds_dict["market_id"] and len(fixture_odds_dict) != 3:
                    z.append(fixture_odds_dict)


    for i in odds_list:
        del i[0]
        if len(i) != 0:
            market = i[0].get("market").replace(" ", "_")
            to_psql(response=i, table=table+"_"+market,
                    engine=engine, if_exists=if_exists)
        else:
            log.info("No odds were included")

    return None

def standardise_columns(response: Union[Dict, List[Dict]], home: str, away: str,
                        home_short: str, away_short: str):
    """
    Standardising the labels through the odds includes.
    For example, Home/Yes, 1/Yes are the same thing,
    just labelled differently.

    Args:
        response:
            Response from SportMonks API; JSON format.
        home:
            Home team.
        away:
            Away team.
        home_short:
            Short code for home team.
        away_short:
            Short code for away team.

    Returns:
        Standardised version of the response from the SportMonks API.

    """
    log.info("Home: %s, Away: %s", home, away)
    if isinstance(response, list):
        label_list = [j.get("label").split("|")[0].strip()
                      for j in response if "|" in j.get("label")]
        log.info("label_list: %s", label_list)
        label_list = list(set(label_list))
        bool_dict = {}
        for team in label_list:
            bool_dict[team] = team in home or team in away
        if "Draw" in bool_dict:
            del bool_dict["Draw"]

        transformed_response = []
        # want the "bankers" to appear first in the list, as the
        # other conditions with the levenshtein distance can
        # be inaccurate
        for k in response:
            if "|" in k.get("label"):
                team = k.get("label").split("|")[0].strip()
                if bool_dict.get(team):
                    transformed_response.insert(0, k)
                else:
                    transformed_response.append(k)
            else:
                transformed_response.append(k)

        for x in transformed_response:
            if "Home" in x.get("label"):
                x["label"] = x.get("label").replace("Home", "1")
            elif "Draw" in x.get("label"):
                x["label"] = x.get("label").replace("Draw", "X")
            elif "Away" in x.get("label"):
                x["label"] = x.get("label").replace("Away", "2")

        for i in transformed_response:

            # Dealing with Bet365 labelling Result/BTTS like:
            # Man United | Yes and so on

            if "|" in i.get("label"):
                team = i.get("label").split("|")[0].strip()
                log.info("Team: %s", team)

                if team == "X":
                    pass
                elif team in home or home in team:
                    log.info("Team: %s is in home: %s", team, home)
                    i["label"] = i.get("label").replace(team, "1")
                    for j in transformed_response:
                        if "|" in j.get("label"):
                            new_team = j.get("label").split("|")[0].strip()
                            if  j != i and new_team != "X" and \
                                team != new_team:
                                log.info("Found away label: %s for away team: %s",
                                         j.get("label"), away)
                                j["label"] = j.get("label").replace(new_team, "2")
                                j["label"] = j.get("label").replace("|", "/").replace(" ", "")
                                log.info("Label: %s", j["label"])
                            elif j != i and team == new_team:
                                log.info("Found other home label: %s for home team: %s",
                                         j.get("label"), home)
                                j["label"] = j.get("label").replace(team, "1")
                                j["label"] = j.get("label").replace("|", "/").replace(" ", "")
                                log.info("Label: %s", j["label"])

                elif team in away or away in team:
                    log.info("Team: %s is in away: %s", team, away)
                    i["label"] = i.get("label").replace(team, "2")
                    for j in transformed_response:
                        if "|" in j.get("label"):
                            new_team = j.get("label").split("|")[0].strip()
                            if  j != i  and new_team != "X" and \
                                team != new_team:
                                log.info("Found home label: %s for home team: %s",
                                         j.get("label"), home)
                                j["label"] = j.get("label").replace(new_team, "1")
                                j["label"] = j.get("label").replace("|", "/").replace(" ", "")
                                log.info("Label: %s", j["label"])
                            elif  j != i and team == new_team:
                                log.info("Found other away label: %s for away team: %s",
                                         j.get("label"), away)
                                j["label"] = j.get("label").replace(team, "2")
                                j["label"] = j.get("label").replace("|", "/").replace(" ", "")
                                log.info("Label: %s", j["label"])
                elif team.upper() == team:
                    # acronym; QPR, PSG
                    log.info("Found acronym: %s", team)
                    if team == home_short:
                        log.info("Acronym in home: %s", home)
                        i["label"] = i.get("label").replace(team, "1")
                    elif team == away_short:
                        log.info("Acronym in away: %s", away)
                        i["label"] = i.get("label").replace(team, "2")
                    else:
                        log.info("What to do with this? TEAM: %s, HS: %s, AS: %s",
                                 team, home_short, away_short)
                elif len(team.split()) > 1:
                    log.info("Team consists of more than one word: %s", team)
                    if len(home.split()) > 1:
                        if (team.split()[0] in home.split()[0]) and \
                        (team.split()[1][0] == home.split()[1][0]):
                            log.debug("IN HOME SPLIT, %s", home)
                            log.debug("TEAM: %s", team)
                            i["label"] = i.get("label").replace(team, "1")
                            i["label"] = i.get("label").replace("|", "/").replace(" ", "")
                            log.info("Label: %s", i["label"])
                            continue
                    if len(away.split()) > 1:
                        if (team.split()[0] in away.split()[0]) and \
                         (team.split()[1][0] == away.split()[1][0]):
                            log.debug("IN AWAY SPLIT, %s", away)
                            log.debug("TEAM: %s", team)
                            i["label"] = i.get("label").replace(team, "2")
                            i["label"] = i.get("label").replace("|", "/").replace(" ", "")
                            log.info("Label: %s", i["label"])
                            continue
                    if enchant.utils.levenshtein(team, home) >= \
                         enchant.utils.levenshtein(team, away):
                        log.info("HOME: %s, AWAY: %s,  TEAM: %s", home, away, team)
                        log.info("CHOSE %s = %s", away, team)
                        i["label"] = i.get("label").replace(team, "2")
                    else:
                        log.info("HOME: %s, AWAY: %s,  TEAM: %s", home, away, team)
                        log.info("CHOSE %s = %s", home, team)
                        i["label"] = i.get("label").replace(team, "1")
                elif enchant.utils.levenshtein(team, home) >= \
                     enchant.utils.levenshtein(team, away):
                    log.info("HOME: %s, AWAY: %s,  TEAM: %s", home, away, team)
                    log.info("CHOSE %s = %s", away, team)
                    i["label"] = i.get("label").replace(team, "2")
                elif enchant.utils.levenshtein(team, home) < enchant.utils.levenshtein(team, away):
                    log.info("HOME: %s, AWAY: %s,  TEAM: %s", home, away, team)
                    log.info("CHOSE %s = %s", home, team)
                    i["label"] = i.get("label").replace(team, "1")

                i["label"] = i.get("label").replace("|", "/").replace(" ", "")
                log.info("Final label: %s", i["label"])

        return transformed_response

    elif isinstance(response, dict):

        if "Home" in response.get("label"):
            response["label"] = response.get("label").replace("Home", "1")
        elif "Draw" in response.get("label"):
            response["label"] = response.get("label").replace("Draw", "X")
        elif "Away" in response.get("label"):
            response["label"] = response.get("label").replace("Away", "2")

        response["label"] = response.get("label").replace("|", "/").replace(" ", "")
        log.info("Final label: %s", response["label"])

        return response

    else:
        raise TypeError(f"Did not expect response of type: {type(response)}")

def fixtures_data_to_sql(start_date: str, end_date: str, league_ids: int, table: str,
                         engine, if_exists: str, markets: Union[int, List[int]] = None,
                         bookmakers: Union[int, List[int]] = None, includes: str = None,
                         cols: Union[str, List[str]] = None, cols_rename: dict = None):

    """
    Insert relevant fixture data in to SQL database.
    Put start_date = end_date if you just want to return fixtures for one day.

    Args:
        start_date:
            Start date of the fixtures you want to load.
            YYYY-MM-DD format.
        end_date:
            End date for the fixtures you want to load.
            YYYY-MM-DD format.
        league_ids:
            What leagues you want the fixture information for.
        table:
            Table name.
        engine:
            sqlalchemy.engine.base.Engine type; connection to database.
        if_exists:
            What to do if the table already exists.
            Must be "fail", "replace" or "append".
        markets: optional.
            What betting markets data you want included.
            If none included, then no betting data will be included.
        bookmakers: optional.
            Which bookmakers you want the betting market data from.
            If non included, then no betting data will be included.
        includes: optional.
            Possible includes: localTeam, visitorTeam, substitutions, goals,
            cards, other, events, corners,lineup, bench, sidelined, comments,
            tvstations, highlights, round, stage, referee, venue, odds,
            inplayOdds, flatOdds, localCoach, visitorCoach, group, trends,
            firstAssistant, secondAssistant,fourthOfficial, stats, shootout, league,
            stats, probability, valuebet.
            ***See Sportmonks.com for information regarding includes.
        cols: optional
            Columns you want in your table.
        cols_rename: optional
            Rename columns.

        Returns:
            None.

    """

    fixtures = sm.get_fixtures_in_date_range(start_date=start_date, end_date=end_date,
                                             league_ids=league_ids, markets=markets,
                                             bookmakers=bookmakers,
                                             includes=includes)

    # want to add fixture data before odds and player data
    # for database integrity purposes (FKs)
    # & want to limit amount of API calls so just make a copy

    fixt_copy = copy.deepcopy(fixtures)
    if isinstance(fixt_copy, list):
        for fixt in fixt_copy:
            if "lineup" in fixt:
                del fixt["lineup"]
            if "odds" in fixt:
                del fixt["odds"]
    elif isinstance(fixt_copy, dict):
        if "lineup" in fixt_copy:
            del fixt_copy["lineup"]
        if "odds" in fixtures:
            del fixt_copy["odds"]

    response = stats_includes(fixt_copy)
    df = pd.json_normalize(response)

    try:
        df = df[cols]
    except KeyError as e:
        log.debug("Key error for columns: %s", e)
        missing_keys = set(cols).difference(df.columns)
        log.info("Missing keys: %s", missing_keys)
        for key in missing_keys:
            df[key] = np.NaN
        df = df[cols]
    finally:
        df.rename(columns=cols_rename, inplace=True)

    with engine.begin() as con:
        to_psql(response=df, table=table, engine=con,
                if_exists=if_exists)
        #con.execute(f"ALTER TABLE public.\"{table}\" ADD PRIMARY KEY (id);")
        #con.execute(f"ALTER TABLE public.\"{table}\" ALTER COLUMN datetime TYPE \
                    #timestamp with time zone using \
                    #to_timestamp(datetime, 'YYYY-MM-DD HH24:MI:SS');")
        con.execute(f"ALTER TABLE public.\"{table}\" ADD COLUMN season text")
        con.execute(f"UPDATE public.\"{table}\"  \
                     SET season = public.\"Seasons\".name \
                     FROM public.\"Seasons\" \
                     WHERE public.\"{table}\".season_id = public.\"Seasons\".id")

        if "odds" in includes:
            odds_includes(fixtures, markets=markets, table=table,
                          if_exists=if_exists, engine=con)

        if "lineup" in includes:
            player_stats = []

            if isinstance(fixtures, list):
                for fixt in fixtures:
                    player_stats += [i for i in fixt.get("lineup")]
            elif isinstance(fixtures, dict):
                player_stats = fixtures["lineup"]
            else:
                raise TypeError(f"Did not expect object of type: {type(fixtures)}")

            to_psql(response=player_stats, table=table+"_players",
                    engine=con, if_exists=if_exists)

    return None

def fixture_to_sql(fixture_ids: Union[int, List[int]], table: str,
                   engine, if_exists: str, markets: list = None,
                   bookmakers: list = None, includes: str = None,
                   cols: List[str] = None, cols_rename: dict = None):

    """Same as above but for specific matches,
       given by their ids."""

    fixtures = sm.get_fixtures_by_ids(fixture_ids=fixture_ids, markets=markets,
                                      bookmakers=bookmakers, includes=includes)

    fixt_copy = copy.deepcopy(fixtures)
    if isinstance(fixt_copy, list):
        for fixt in fixt_copy:
            if "lineup" in fixt:
                del fixt["lineup"]
            if "odds" in fixt:
                del fixt["odds"]
    elif isinstance(fixt_copy, dict):
        if "lineup" in fixt_copy:
            del fixt_copy["lineup"]
        if "odds" in fixtures:
            del fixt_copy["odds"]

    response = stats_includes(fixt_copy)
    df = pd.json_normalize(response)

    try:
        df = df[cols]
    except KeyError as e:
        log.debug("Key error for columns: %s", e)
        missing_keys = set(cols).difference(df.columns)
        log.info("Missing keys: %s", missing_keys)
        for key in missing_keys:
            df[key] = np.NaN
        df = df[cols]
    finally:
        df.rename(columns=cols_rename, inplace=True)

    with engine.begin() as con:
        to_psql(response=df, table=table, engine=con,
                if_exists=if_exists)
        #con.execute(f"ALTER TABLE public.\"{table}\" ADD PRIMARY KEY (id);")
        #con.execute(f"ALTER TABLE public.\"{table}\" ALTER COLUMN datetime TYPE \
                    #timestamp with time zone using \
                    #to_timestamp(datetime, 'YYYY-MM-DD HH24:MI:SS');")
        con.execute(f"ALTER TABLE public.\"{table}\" ADD COLUMN season text")
        con.execute(f"UPDATE public.\"{table}\"  \
                     SET season = public.\"Seasons\".name \
                     FROM public.\"Seasons\" \
                     WHERE public.\"{table}\".season_id = public.\"Seasons\".id")

        if "odds" in includes:
            odds_includes(fixtures, markets=markets, table=table,
                          if_exists=if_exists, engine=con)

        if "lineup" in includes:
            player_stats = []

            if isinstance(fixtures, list):
                for fixt in fixtures:
                    player_stats += [i for i in fixt.get("lineup")]
            elif isinstance(fixtures, dict):
                player_stats = fixtures["lineup"]
            else:
                raise TypeError(f"Did not expect object of type: {type(fixtures)}")

            to_psql(response=player_stats, table=table+"_players",
                    engine=con, if_exists=if_exists)

    return None
