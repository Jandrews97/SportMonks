"""SportMonks Football API"""

import os
import logging
from typing import Dict, Optional, Union, List, Any
import numpy as np
import pandas as pd
from base import BaseAPI
import helper
from errors import IncompatibleArgs, NotJSONNormalizable

log = helper.setup_logger(__name__, "SM_API.log")
KEY = os.environ.get("SportMonks_API_KEY")

class Continents(BaseAPI):
    """Continents Class."""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def continents(self, continent_id: Optional[int] = None,
                   includes: Optional[Union[str, List[str]]] = None,
                   df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        The leagues endpoint helps you with assigning Countries and Leagues
        to the part of the world (Continent) they belong to.
        Available leagues are Europe, Asia, Africa, Oceania,
        North America and South America.

        Args:
            continent_id:
                id of the continent you want to retrieve.
                If no continent_id is specified, all leagues will be returned.
            df:
                if you want it in a Pandas DataFrame (if possible).
            includes:
                Possible includes: countries.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """


        if continent_id:
            log.info("Get continent by id: %s, with includes = %s", continent_id, includes)
            continents = self.make_request(endpoint=["continents", continent_id], includes=includes)
            if df:
                try:
                    df_continents = self._to_df(continents, cols=df_cols)
                    return df_continents
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON instead.")
                    return continents
            else:
                return continents
        else:
            log.info("Get all continents")
            continents = self.make_request(endpoint="continents", includes=includes)
            if df:
                try:
                    continents = self._to_df(continents, cols=df_cols)
                    return continents
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON instead.")
                    return continents
            else:
                return continents
            log.info("Returned %s leagues with includes = %s", len(continents), includes)

class Countries(BaseAPI):
    """Countries Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def countries(self, country_id: Optional[int] = None,
                  includes: Optional[Union[str, List[str]]] = None,
                  df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        The Countries endpoint provides you Country information
        like for example its Flag, IsoCode, Continent and other related Country information.
        If no country id is specified, all countries will be returned

        Args:
            country_id:
                id of the country you want to retrieve.
                If no country_id is specified, all countries will be returned.
            includes:
                Possible includes: leagues, continent.
                ***See Sportmonks.com for information regarding includes.


        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        if country_id:
            log.info("Returning country by id: %s, with includes = %s", country_id, includes)
            countries = self.make_request(endpoint=["countries", country_id], includes=includes)
            if df:
                try:
                    df_countries = self._to_df(countries, cols=df_cols)
                    return df_countries
                except NotJSONNormalizable:
                    log.info("Not JSON-noralizable, returning JSON instead.")
                    return countries
            else:
                return countries
        else:
            log.info("Returning all countries")
            countries = self.make_request(endpoint="countries", includes=includes)
            if df:
                try:
                    df_countries = self._to_df(countries, cols=df_cols)
                    return df_countries
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON instead.")
                    return countries
            else:
                return countries

class Leagues(BaseAPI):
    """Leagues Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def by_id(self, league_id: Optional[int] = None,
              includes: Optional[Union[str, List[str]]] = None,
              df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        A request on this endpoint would return a response with all Leagues you have access to,
        based on the plan you are subscribed to. The Leagues endpoint provides you
        League information like its ID, Name, Country, Coverage etc.
        If no league id is specified, all leagues in your plan will be returned

        Args:
            league_id:
                id of the league you want to retrieve.
                If no league_id is specified, all leagues in your plan will be returned.
            includes:
                Possible includes: country, season, seasons.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        if league_id:
            log.info("Return a league by id: %s, with includes = %s", league_id, includes)
            leagues = self.make_request(endpoint=["leagues", league_id], includes=includes)
            if df:
                try:
                    df_leagues = self._to_df(leagues, cols=df_cols)
                    return df_leagues
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable; returning JSON instead.")
                    return leagues
            else:
                return leagues
        else:
            log.info("Returning all leagues")
            leagues = self.make_request(endpoint="leagues", includes=includes)
            if df:
                try:
                    df_leagues = self._to_df(leagues, cols=df_cols)
                    return df_leagues
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable; returning JSON instead.")
                    return leagues
            else:
                return leagues


    def by_name(self, search: str, includes: Optional[Union[str, List[str]]] = None,
                df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        A request on this endpoint would return a response with all Leagues you have access to,
        based on the plan you are subscribed to. The Leagues endpoint provides you
        League information like its ID, Name, Country, Coverage etc.
        If no league id is specified, all leagues in your plan will be returned

        Args:
            name:
                name of the league
            includes:
                Possible includes: country, season, seasons.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        log.info("Returning a league by search: %s", search)
        leagues = self.make_request(endpoint=["leagues", "search", search], includes=includes)
        if df:
            try:
                df_leagues = self._to_df(leagues, cols=df_cols)
                return df_leagues
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable; returning JSON.")
                return leagues
        else:
            return leagues

class Seasons(BaseAPI):
    """Seasons API"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)


    def seasons(self, season_id: Optional[int] = None,
                includes: Optional[Union[str, List[str]]] = None,
                df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        Responses of the Seasons endpoint are limited to Seasons of the Leagues available in the
        Plan you are subscribed to.
        Responses provide you details about for example the Season ID, Name, League ID, Year and
        if the Season is Active Yes or No.
        If no season id is specified, all seasons will be returned

        Possible includes: league, stages, rounds, upcoming, results,
        groups, goalscorers, cardscorers,assistscorers,
        aggregatedGoalscorers, aggregatedCardscorers, aggregatedAssistscorers, fixtures
        + stage, round IF season_id SPECIFIED

        Args:
            season_id: optional
                id of the season you want to retrieve.
                If no season id is specified, all seasons will be returned.
            includes: optional
                Possible includes: league, stages, rounds, upcoming, results,
                groups, goalscorers, cardscorers,assistscorers, aggregatedGoalscorers,
                aggregatedCardscorers, aggregatedAssistscorers, fixtures
                + stage, round IF season_id is specified.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        if season_id:
            log.info("Returning season by id: %s, with includes = %s", season_id, includes)
            seasons = self.make_request(endpoint=["seasons", season_id], includes=includes)
            if df:
                try:
                    df_seasons = self._to_df(seasons, cols=df_cols)
                    return df_seasons
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable; returning JSON instead.")
                    return seasons
            else:
                return seasons
        else:
            log.info("Returning all seasons")
            seasons = self.make_request(endpoint="seasons", includes=includes)
            if df:
                try:
                    df_seasons = self._to_df(seasons, cols=df_cols)
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable; returning JSON instead.")
                    return seasons
            else:
                return seasons


class Bookmakers(BaseAPI):
    """Bookmakers Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)


    def bookmakers(self, bookmaker_id: Optional[int] = None,
                   df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        Return a bookmaker by id.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            bookmaker_id: optional
                id of the bookmaker you want to retrieve.
                If no bookmaker_id is specified, then all will be returned.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        if bookmaker_id:
            log.info("Returning bookmaker by id: %s", bookmaker_id)
            bookmakers = self.make_request(endpoint=["bookmakers", bookmaker_id])
            if df:
                try:
                    df_bookmakers = self._to_df(bookmakers, cols=df_cols)
                    return df_bookmakers
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return bookmakers
            else:
                return bookmakers

        else:
            log.info("Returning all bookmakers")
            bookmakers = self.make_request(endpoint="bookmakers")
            if df:
                try:
                    df_bookmakers = self._to_df(bookmakers, cols=df_cols)
                    return df_bookmakers
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return bookmakers
            else:
                return bookmakers

class Markets(BaseAPI):
    """Markets Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def markets(self, market_id: Optional[int] = None,
                df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        Markets represent the betting options available per bookmaker.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            market_id:
                id of the market you want to return.
                If no market_id is specified, all markets will be returned.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        if market_id:
            log.info("Returning market: %s", market_id)
            markets = self.make_request(endpoint=["markets", market_id])
            if df:
                try:
                    df_markets = self._to_df(markets, cols=df_cols)
                    return df_markets
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON")
                    return markets
            else:
                return markets
        else:
            markets = self.make_request(endpoint="markets")
            log.info("Returning all markets; %s markets", len(markets))
            if df:
                try:
                    df_markets = self._to_df(markets, cols=df_cols)
                    return df_markets
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON")
                    return markets
            else:
                return markets

class Teams(BaseAPI):
    """Teams Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def by_id(self, team_id: int, includes: Optional[Union[str, List[str]]] = None,
              df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        With the Teams endpoint you can find all Team Details you need.
        You can think of information about when the Team is founded, Logo, Team Name,
        Short Name etc.

        Args:
            team_id:
                id of the team you want to return.
            includes:
                Possible includes: country, squad, coach, transfers, sidelined,
                stats, venue, fifaranking,uefaranking, visitorFixtures, localFixtures,
                visitorResults, latest, upcoming, goalscorers,
                cardscorers, assistscorers, aggregatedGoalscorers, aggregatedCardscorers,
                aggregatedAssistscorers, league, activeSeasons, trophies.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.
        """
        team = self.make_request(endpoint=["teams", team_id], includes=includes)
        if df:
            try:
                df_team = self._to_df(team, cols=df_cols)
                return df_team
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return team
        else:
            return team


    def by_season_id(self, season_id: int, includes: Optional[Union[str, List[str]]] = None,
                     df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        With the Teams endpoint you can find all Team Details you need.
        You can think of information about when the Team is founded, Logo, Team Name,
        Short Name etc.

        Args:
            season:
                id of the season you want to return.
            includes:
                Possible includes: country, squad, coach, transfers, sidelined,
                stats, venue, fifaranking,uefaranking, visitorFixtures, localFixtures,
                visitorResults, latest, upcoming, goalscorers,
                cardscorers, assistscorers, aggregatedGoalscorers, aggregatedCardscorers,
                aggregatedAssistscorers, league, activeSeasons, trophies.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.
        """

        teams = self.make_request(endpoint=["teams", "season", season_id], includes=includes)
        if df:
            try:
                df_teams = self._to_df(teams, cols=df_cols)
                return df_teams
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return teams
        else:
            return teams

    def team_current_leagues(self, team_id: int, df: bool = False,
                             df_cols: Optional[Union[str, List[str]]] = None):
        """
        Return all current leagues for a given team.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            team_id:
                id of the team.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        current_leagues = self.make_request(endpoint=["teams", team_id, "current"])
        if df:
            try:
                df_current_leagues = self._to_df(current_leagues, cols=df_cols)
                return df_current_leagues
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return current_leagues
        else:
            return current_leagues


    def team_historic_leagues(self, team_id, df: bool = False,
                              df_cols: Optional[Union[str, List[str]]] = None):
        """
        Return all historic leagues for a given team.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            team_id:
                id of the team

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        historic_leagues = self.make_request(endpoint=["teams", team_id, "history"])
        if df:
            try:
                df_historic_leagues = self._to_df(historic_leagues, cols=df_cols)
                return df_historic_leagues
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return historic_leagues
        else:
            return historic_leagues

    def squads(self, season_id: int, team_id: int,
               includes: Optional[Union[str, List[str]]] = None,
               df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        Since November 2017 we offer the ability to load historical Squads.
        This means you can retrieveSquads from 2005 onwards, including
        Player performance of those Games of the requested Season.

        The squad include on any team related endpoint or include will only return
        the squad ofthe current season of the domestic league
        the team is playing in. You can use this endpoint to load squads for a
        different season or even for cups.

        Args:
            season_id:
                id of the season
            team_id:
                id of the team
            includes:
                player

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.
        """
        squads = self.make_request(endpoint=["squad", "season", season_id, "team", team_id],
                                   includes=includes)
        if df:
            try:
                df_squads = self._to_df(squads, cols=df_cols)
                return df_squads
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return squads
        else:
            return squads


    def head2head(self, team1_id: int, team2_id: int,
                  includes: Optional[Union[str, List[str]]] = None,
                  df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        The Head 2 Head endpoint provides you all previous Games between 2 Teams

        Args:
            team1_id:
                id of team 1.
            team2_id:
                id of team 2.
            includes: optional
                Possible includes: localTeam, visitorTeam, substitutions, goals, cards,
                other, events, corners,lineup, bench, sidelined, comments, tvstations,
                highlights, round, stage, referee, venue, odds,
                inplayOdds, flatOdds, localCoach, visitorCoach, group, trends.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        h2h = self.make_request(endpoint=["head2head", team1_id, team2_id], includes=includes)

        if df:
            try:
                df_h2h = self._to_df(h2h, cols=df_cols)
                return df_h2h
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return h2h
        else:
            return h2h

    def head2head_results(self):
        """Placeholder"""
        return None

class Commentaries(BaseAPI):
    """Commentaries Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def commentaries(self, fixture_id: int, df: bool = False,
                     df_cols: Optional[Union[str, List[str]]] = None):
        """
        The Commentary endpoint can be used to request the Textual representation of
        actions taken place in the Game.
        Commentaries are marked as Important or Goal when they meet that criteria.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            fixture_id:
                id of the fixture

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.
        """
        commentaries = self.make_request(endpoint=["commentaries", "fixture", fixture_id])[::-1]
        if df:
            try:
                df_commentaries = self._to_df(commentaries, cols=df_cols)
                return df_commentaries
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return commentaries
        else:
            return commentaries

class Venues(BaseAPI):
    """Venues class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def by_id(self, venue_id: int, df: bool = False,
              df_cols: Optional[Union[str, List[str]]] = None):

        """
        The Venue endpoint provides Venue information like Name, City,
        Capacity, Address and even a Venue image.
        If venue_id supplied, then info will be returned for that venue.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            venue_id:
                id of the venue you want to return.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        venue = self.make_request(endpoint=["venues", venue_id])
        if df:
            try:
                df_venue = self._to_df(venue, cols=df_cols)
                return df_venue
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return venue
        else:
            return venue


    def by_season(self, season_id: int, df: bool = False,
                  df_cols: Optional[Union[str, List[str]]] = None):
        """
        The Venue endpoint provides Venue information like Name, City,
        Capacity, Address and even a Venue image.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            season_id:
                id of the season you want to retrieve venues for.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        venues = self.make_request(endpoint=["venues", "season", season_id])
        if df:
            try:
                df_venues = self._to_df(venues, cols=df_cols)
                return df_venues
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return venues
        else:
            return venues

class Coaches(BaseAPI):
    """Coaches Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def coaches(self, coach_id: int, df: bool = False,
                df_cols: Optional[Union[str, List[str]]] = None):

        """
        The Coaches endpoint provides you details about the Coach like its Name,
        Nationality Birthdate etc. By default this endpoint returns Coach details that
        have hosted at least 1 game under the Leagues covered by the
        plan you are subscribed to.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            coach_id:
                id of the coach you want to return.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        coach = self.make_request(endpoint=["coaches", coach_id])
        if df:
            try:
                df_coach = self._to_df(coach, cols=df_cols)
                return df_coach
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return coach
        else:
            return coach

class Rounds(BaseAPI):
    """Rounds Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def by_round(self, round_id: int,
                 includes: Optional[Union[str, List[str]]] = None,
                 df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        Leagues can be split up in Rounds representing a week a game is played in.
        With this endpoint we give you the ability to request data for a single
        Round as well as all Rounds of a Season. The endpoint is often used in
        combination with includes like Results or Fixtures to show them based on Rounds.

        Args:
            round_id:
                id of the round you want returning.
            includes:
                Possible includes: fixtures, results, season, league.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        rounds = self.make_request(endpoint=["rounds", round_id], includes=includes)
        if df:
            try:
                df_rounds = self._to_df(rounds, cols=df_cols)
                return df_rounds
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return rounds
        else:
            return rounds

    def by_season(self, season_id: int,
                  includes: Optional[Union[str, List[str]]] = None,
                  df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        Leagues can be split up in Rounds representing a week a game is played in.
        With this endpoint we give you the ability to request data for a single
        Round as well as all Rounds of a Season. The endpoint is often used in
        combination with includeslike Results or Fixtures to show them based on Rounds.
        Returns ids of the gameweeks for the season.

        Args:
            season_id:
                id of the season you want returning.
            includes:
                Possible includes: fixtures, results, season, league.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        rounds = self.make_request(endpoint=["rounds", "season", season_id],
                                   includes=includes)
        if df:
            try:
                df_rounds = self._to_df(rounds, cols=df_cols)
                return df_rounds
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return rounds
        else:
            return rounds

class Stages(BaseAPI):
    """Stages Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def by_stage(self, stage_id: int, includes: Optional[Union[str, List[str]]] = None,
                 df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        Leagues and Seasons all over the world can have a different set up.
        The Stages endpoint can help you to define the current
        Stage or set up of multiple Stages of a particular League/Season.
        Stages names are for example: Regular Season, Play-offs, Semi-Finals, Final etc.

        Args:
            stage_id:
                id of the stage you want to return info from.
            includes:
                Possible includes: fixtures, results, season, league

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.
        """

        stages = self.make_request(endpoint=["stages", stage_id], includes=includes)
        if df:
            try:
                df_stages = self._to_df(stages, cols=df_cols)
                return df_stages
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return stages
        else:
            return stages


    def by_season(self, season_id: int, includes: Optional[Union[str, List[str]]] = None,
                  df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        Leagues and Seasons all over the world can have a different set up.
        The Stages endpoint can help you to define the current
        Stage or set up of multiple Stages of a particular League/Season.
        Stages names are for example: Regular Season, Play-offs, Semi-Finals, Final etc.

        Args:
            season_id:
                id of the season you want to return info from.
            includes:
                Possible includes: fixtures, results, season, league

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.
        """

        seasons = self.make_request(endpoint=["stages", "season", season_id], includes=includes)
        if df:
            try:
                df_seasons = self._to_df(seasons, cols=df_cols)
                return df_seasons
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return seasons
        else:
            return seasons

class Players(BaseAPI):
    """Players Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def by_id(self, player_id: int, includes: Optional[Union[str, List[str]]] = None,
              df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        The Players endpoint provides you detailed Player information.
        With this endpoint you will be able to build a complete Player Profile.

        Args:
            player_id:
                id of the player.
            includes: optional
                Possible includes: position, team, stats, trophies,
                sidelined, transfers, lineups, country.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

       """

        player = self.make_request(endpoint=["players", player_id], includes=includes)
        if df:
            try:
                df_player = self._to_df(player, cols=df_cols)
                return df_player
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return player
        else:
            return player

    def by_name(self, search: str, includes: Optional[Union[str, List[str]]] = None,
                df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        The Players endpoint provides you detailed Player information.
        With this endpoint you will be able to build a complete Player Profile.

        Args:
            search:
                name of the player.
            includes: optional
                Possible includes: position, team, stats, trophies,
                sidelined, transfers, lineups, country.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

       """

        players = self.make_request(endpoint=["players", "search", search], includes=includes)
        if df:
            try:
                df_players = self._to_df(players, cols=df_cols)
                return df_players
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return players
        else:
            return players

class Fixtures(BaseAPI):
    """Fixtures Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    @staticmethod
    def __stats_includes(response: Union[dict, List[dict]]):
        """Placeholder"""

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

    def by_id(self, fixture_ids: Union[int, List[int]],
              markets: Optional[Union[int, List[int]]] = None,
              bookmakers: Optional[Union[int, List[int]]] = None,
              includes: Optional[Union[str, List[str]]] = None,
              df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        The Fixture endpoint provides information about Games in particular Leagues.
        There are always 2 teams involved in a Fixture.

        Args:
            fixture_ids:
                ids of the fixtures you want to return.
            markets: optional
                Filter odds based on the list of market ids.
                If no markets specified, then all will be returned.
            bookmakers: optional
                Filter odds based on the list of bookmaker ids.
                If no bookmakers are specified, then all will be returned.
            includes: optional
                Possible includes: localTeam, visitorTeam, substitutions, goals, cards,
                other, events, corners,lineup, bench, sidelined, comments, tvstations,
                highlights, round, stage, referee, venue, odds,
                inplayOdds, flatOdds, localCoach, visitorCoach, group, trends, firstAssistant,
                secondAssistant,fourthOfficial, stats, shootout,
                league, stats, probability, valuebet.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        params = {"markets": markets, "bookmakers": bookmakers}
        log.info("Params in fixtures: %s", params)

        if isinstance(fixture_ids, list):
            fixture_ids = ",".join(list(map(str, fixture_ids)))
            fixtures = self.make_request(endpoint=["fixtures", "multi", fixture_ids],
                                         includes=includes, params=params)
            if df:
                try:
                    df_fixtures = self._to_df(fixtures, cols=df_cols)
                    return df_fixtures
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return fixtures
            else:
                return fixtures
        else:
            fixtures = self.make_request(endpoint=["fixtures", fixture_ids],
                                         includes=includes, params=params)
            if df:
                try:
                    df_fixtures = self._to_df(fixtures, cols=df_cols)
                    return df_fixtures
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return fixtures
            else:
                return fixtures

    def by_date(self, date: str, league_ids: Optional[Union[int, List[int]]] = None,
                markets: Optional[Union[int, List[int]]] = None,
                bookmakers: Optional[Union[int, List[int]]] = None,
                includes: Optional[Union[str, List[str]]] = None,
                df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        Fixtures by date.

        Args:
            date:
                Date of the fixtures you want to return.
                YYYY-MM-DD format.
            league_ids: optional.
                ids of the leagues you want the fixtures for.
                If no league_id included, then all fixtures for leagues
                in your plan will be returned.
            markets: optional
                ids of the markets you want to return for the given fixtures.
                If none included, then all markets will be returned.
            bookmakers: optional
                ids of the bookmakers you want to return for the given fixtures.
                If none included, then all bookmakers will be returned.
            includes: optional
                Possible includes: localTeam, visitorTeam, substitutions, goals,
                cards, other, events, corners,lineup, bench, sidelined, comments,
                tvstations, highlights, round, stage, referee, venue, odds,
                inplayOdds, flatOdds, localCoach, visitorCoach, group, trends,
                firstAssistant, secondAssistant, fourthOfficial, stats, shootout,
                league, stats, probability, valuebet.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        params = {"leagues": league_ids, "markets": markets, "bookmakers": bookmakers}

        fixtures = self.make_request(endpoint=["fixtures", "date", date],
                                     includes=includes, params=params)
        if df:
            try:
                df_fixtures = self._to_df(fixtures, cols=df_cols)
                return df_fixtures
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return fixtures
        else:
            return fixtures

    def by_date_range(self, start_date: str, end_date: str,
                      team_id: Optional[int] = None,
                      league_ids: Optional[Union[int, List[int]]] = None,
                      markets: Optional[Union[int, List[int]]] = None,
                      bookmakers: Optional[Union[int, List[int]]] = None,
                      includes: Optional[Union[str, List[str]]] = None,
                      df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        Fixtures between start_date and end_date.

        Args:
            start_date:
                Start date of fixtures you want returning.
            end_date:
                End date of the fixtures you want returning.
            team_id: optional
                id of the team's fixtures you want returning.
                If no team_id specified, then all teams will be returned.
            league_ids: optional
                ids of the leagues you want returning.
                If non specified, then all will be returned.
            markets: optional
                ids of the markets you want returned.
                If none specified, then all markets will be returned.
            bookmakers: optional
                ids of the bookmakers you want returned.
                If non specified, then all bookmakers will be returned.
            includes: optional
                Possible includes: localTeam, visitorTeam, substitutions, goals,
                cards, other, events, corners,lineup, bench, sidelined, comments,
                tvstations, highlights, round, stage, referee, venue, odds,
                inplayOdds, flatOdds, localCoach, visitorCoach, group, trends,
                firstAssistant, secondAssistant,fourthOfficial, stats, shootout, league,
                stats, probability, valuebet.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        params = {"leagues": league_ids, "markets": markets, "bookmakers": bookmakers}

        if team_id:
            fixtures = self.make_request(endpoint=["fixtures", "between", start_date, end_date,
                                                   team_id],
                                         includes=includes, params=params)
            if df:
                try:
                    df_fixtures = self._to_df(fixtures, cols=df_cols)
                    return df_fixtures
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return fixtures
            else:
                return fixtures
        else:
            fixtures = self.make_request(endpoint=["fixtures", "between", start_date, end_date],
                                         includes=includes, params=params)
            if df:
                try:
                    df_fixtures = self._to_df(fixtures, cols=df_cols)
                    return df_fixtures
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return fixtures
            else:
                return fixtures

    def inplay_fixtures(self, markets: Optional[Union[int, List[int]]] = None,
                        bookmakers: Optional[Union[int, List[int]]] = None,
                        league_ids: Optional[Union[int, List[int]]] = None,
                        includes: Optional[Union[str, List[str]]] = None,
                        df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        Games currently being played

        Args:
            markets: optional
                ids of the markets you want returned.
                If none specified, then all will be returned.
            bookmakers: optional
                ids of the bookmakers you want returned.
                If none specified, then all will be returned.
            league_ids: optional
                ids of the leagues you want returned.
                If none specified, then all will be returned.
            includes: optional
                Possible includes: localTeam, visitorTeam, substitutions, goals,
                cards, other, events, corners, lineup, bench, sidelined, comments,
                tvstations, highlights, round, stage, referee, venue, odds,
                inplayOdds, flatOdds, localCoach, visitorCoach, group, trends,
                firstAssistant, secondAssistant, fourthOfficial, stats,
                shootout, league, stats, probability, valuebet.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        params = {"leagues": league_ids, "markets": markets, "bookmakers": bookmakers}
        fixtures = self.make_request(endpoint=["livescores", "now"], includes=includes,
                                     params=params)
        if df:
            try:
                df_fixtures = self._to_df(fixtures, cols=df_cols)
                return df_fixtures
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return fixtures
        else:
            return fixtures


    def fixture_stats(self, fixture_ids: Union[int, List[int]],
                      includes: Optional[Union[str, List[str]]] = None,
                      cols: Optional[Union[str, List[str]]] = None):
        """
        Fixture statistics to a pandas DataFrame.
        Recommended includes are:
        league.country,localTeam,visitorTeam,localCoach,visitorCoach,venue,referee,stats
        """

        response = self.by_id(fixture_ids=fixture_ids, includes=includes)

        if "stats" in includes:
            response = self.__stats_includes(response)

        return self._to_df(response, cols=cols)

class Schedule(BaseAPI):
    """Schedule (today) Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def schedule_today(self, markets: Optional[Union[int, List[int]]] = None,
                       bookmakers: Optional[Union[int, List[int]]] = None,
                       league_ids: Optional[Union[int, List[int]]] = None,
                       includes: Optional[Union[str, List[str]]] = None,
                       df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        Returns the schedule for the current day.

        Args:
            markets: optional
                ids of the markets you want returned.
                If none specified, then all will be returned.
            bookmakers: optional
                ids of the bookmakers you want returned.
                If none specified, then all will be returned.
            league_ids: optional
                ids of the leagues you want returned.
                If none specified, then all will be returned.
            includes: optional
                Possible includes: localTeam, visitorTeam, substitutions, goals,
                cards, other, events, corners,lineup, bench, sidelined, comments,
                tvstations, highlights, round, stage, referee, venue, odds,
                inplayOdds, flatOdds, localCoach, visitorCoach, group, trends,
                firstAssistant, secondAssistant,fourthOfficial, stats,
                shootout, league, stats, probability, valuebet.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        params = {"leagues": league_ids, "markets": markets, "bookmakers": bookmakers}
        schedule = self.make_request(endpoint="livescores", includes=includes, params=params)
        if df:
            try:
                df_schedule = self._to_df(schedule, cols=df_cols)
                return df_schedule
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return schedule
        else:
            return schedule

class Standings(BaseAPI):
    """Standings Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def by_season(self, season_id: int, includes: Optional[Union[str, List[str]]] = None,
                  group_ids: Optional[Union[int, List[int]]] = None,
                  stage_ids: Optional[Union[int, List[int]]] = None,
                  df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        Standings represent the rankings of Teams in the different Leagues they participate.
        Responses of the Standings endpoint can be returned in 2 formats,
        depending on the League setup. For ‘normal’ Leagues the response
        format is different compared to Cups.

        Args:
            season_id:
                id of the season you want the standings for.
            group_ids: optional
                Specifies which group to return the standings.
                For example, group A in UCL.
            stage_ids: optional
                Stage of the season you want to return standings for.
            includes: optional
                Possible includes: standings.team, standings.league, standings.season,
                standings.round, standings.stages.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        params = {"stage_ids": stage_ids, "group_ids": group_ids}
        standings = self.make_request(endpoint=["standings", "season", season_id],
                                      includes=includes, params=params)
        if df:
            try:
                df_standings = self._to_df(standings, cols=df_cols)
                return df_standings
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return standings
        else:
            return standings

    def by_date(self, season_id: int, date: str,
                df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):
        """
        With this endpoint you are able to retrieve the standings at a given date(time).
        It will calculate the games played up until the given date/time and
        provide a standings result for it.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            season_id:
                id of the season you want to return.
            date:
                Date of the season you want standings up to.
                For example, 2016-01-01 would return standings
                halfway (roughly) through 2015/2016 season.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        standings = self.make_request(endpoint=["standings", "season", season_id, "date", date])
        if df:
            try:
                df_standings = self._to_df(standings, cols=df_cols)
                return df_standings
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return standings
        else:
            return standings

class TopScorers(BaseAPI):
    """Topscorers Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def topscorers(self, season_id: int, stage_ids: Optional[Union[int, List[int]]] = None,
                   includes: Optional[Union[str, List[str]]] = None,
                   df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        The Topscorers endpoint provides you accurate information about the Topscorers in Goals,
        Cards and Assists. The endpoint returns the top 25 players and they can
        all be included at once or separately per Type (Goals, Cards or Assists).
        Stage could be regular season, semi final, final and so on.
        This Topscorers endpoint returns the Topscorers by Stage of the Season.
        If you want an aggregated Topscorer list,
        please use the Aggregated Topscorers by Season endpoint.

        Args:
            season_id:
                id of the season you want topscorers for.
            stage_ids: optional
                ids of the stage you want topscorers for.
            includes: optional
                Possible includes: goalscorers.player, goalscorers.team,
                assistscorers.player, assistscorers.team, cardscorers.player,
                cardscorers.team.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        params = {"stage_ids": stage_ids}
        topscorers = self.make_request(endpoint=["topscorers", "season", season_id],
                                       includes=includes, params=params)
        if df:
            try:
                df_topscorers = self._to_df(topscorers, cols=df_cols)
                return df_topscorers
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return topscorers
        else:
            return topscorers

    def aggregated_topscorers(self, season_id: int,
                              includes: Optional[Union[str, List[str]]] = None,
                              df: bool = False, df_cols: Optional[Union[str, List[str]]] = None):

        """
        This Topscorers endpoint returns the Aggregated Topscorers by Season.
        This means that all stages are summed, also preliminary stages.

        Args:
            season_id:
                id of the season you want topscorers for.
            includes: optional
                Possible includes: aggregatedGoalscorers.player, aggregatedGoalscorers.team,
                aggregatedAssistscorers.player, aggregatedAssistscorers.team,
                aggregatedCardscorers.player, aggregatedCardscorers.team.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        topscorers = self.make_request(endpoint=["topscorers", "season", season_id, "aggregated"],
                                       includes=includes)
        if df:
            try:
                df_topscorers = self._to_df(topscorers, cols=df_cols)
                return df_topscorers
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return topscorers
        else:
            return topscorers

class Odds(BaseAPI):
    """Odds Class"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def odds(self, fixture_id: int, bookmaker_id: Optional[int] = None,
             market_id: Optional[int] = None, df: bool = False,
             df_cols: Optional[Union[str, List[str]]] = None):

        """
        Odds are used to add betting functionality to your application.
        This endpoint can be used for Pre-match Odds,
        although we also have an endpoint for In-Play Odds (live).
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT.

        Args:
            fixture_id:
                id of the fixture you want odds for.
            bookmaker_id:
                id of the bookmaker you want odds info from.
            market_id:
                id of the market you want odds info from.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        if bookmaker_id and market_id:
            raise IncompatibleArgs("No endpoint for market and bookmaker id. Use \
                                   the fixtures includes with markets and bookmaker params.")
        elif bookmaker_id:
            odds = self.make_request(endpoint=["odds", "fixture", fixture_id,
                                               "bookmaker", bookmaker_id])
            if df:
                try:
                    df_odds = self._to_df(odds, cols=df_cols)
                    return df_odds
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return odds
            else:
                return odds

        elif market_id:
            odds = self.make_request(endpoint=["odds", "fixture", fixture_id,
                                               "market", market_id])
            if df:
                try:
                    df_odds = self._to_df(odds, cols=df_cols)
                    return df_odds
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return odds
            else:
                return odds
        else:
            odds = self.make_request(endpoint=["odds", "fixture", fixture_id])
            if df:
                try:
                    df_odds = self._to_df(odds, cols=df_cols)
                    return df_odds
                except NotJSONNormalizable:
                    log.info("Not JSON-normalizable, returning JSON.")
                    return odds
            else:
                return odds

    def live_odds(self, fixture_id: int, df: bool = False,
                  df_cols: Optional[Union[str, List[str]]] = None):
        """
        In play odds by fixture
        ***MUST HAVE ADVANCED SPORTMONKS PLAN
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            fixture_id:
                id of the fixture you want live odds for.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        odds = self.make_request(endpoint=["odds", "inplay", "fixture", fixture_id])
        if df:
            try:
                df_odds = self._to_df(odds, cols=df_cols)
                return df_odds
            except NotJSONNormalizable:
                log.info("Not JSON-normalizable, returning JSON.")
                return odds
        else:
            return odds
