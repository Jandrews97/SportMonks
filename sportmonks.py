"""
Wrapper for SportMonks API
"""
import logging
from typing import Dict, Optional, Union, List, Any
import numpy as np
import pandas as pd
import requests
from connection import get_data
import helper

log = helper.setup_logger(__name__, "SM_API.log")

def get_continents(continent_id: int = None, includes: str = None):
    """
    The Continents endpoint helps you with assigning Countries and Leagues
    to the part of the world (Continent) they belong to.
    Available Continents are Europe, Asia, Africa, Oceania,
    North America and South America.

    Args:
        continent_id: optional
            id of the continent you want to retrieve.
            If no continent_id is specified, all continents will be returned.
        includes: optional
            Possible includes: countries.
            ***See Sportmonks.com for information regarding includes.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    if continent_id:
        log.info("Get continent by id: %s, with includes = %s", continent_id, includes)
        return get_data(endpoint=f"continents/{continent_id}", includes=includes)
    else:
        log.info("Get all continents")
        continents = get_data(endpoint="continents", includes=includes)
        log.info("Returned %s continents with includes = %s", len(continents), includes)
        return continents

def get_countries(country_id: int = None, includes: str = None):
    """
    The Countries endpoint provides you Country information
    like for example its Flag, IsoCode, Continent and other related Country information.
    If no country id is specified, all countries will be returned

    Args:
        country_id: optional
            id of the country you want to retrieve.
            If no country_id is specified, all countries will be returned.
        includes: optional
            Possible includes: leagues, continent.
            ***See Sportmonks.com for information regarding includes.


    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    if country_id:
        log.info("Returning country by id: %s, with includes = %s", country_id, includes)
        return get_data(endpoint=f"countries/{country_id}", includes=includes)
    else:
        log.info("Get all countries")
        countries = get_data(endpoint="countries", includes=includes)
        log.info("Returned %s countries with includes = %s", len(countries), includes)
        return countries

def get_leagues(league_id: int = None, includes: str = None):
    """
    A request on this endpoint would return a response with all Leagues you have access to,
    based on the plan you are subscribed to. The Leagues endpoint provides you League information
    like its ID, Name, Country, Coverage etc.
    If no league id is specified, all leagues in your plan will be returned

    Args:
        league_id: optional.
            id of the league you want to retrieve.
            If no league_id is specified, all leagues in your plan will be returned.
        includes: optional
            Possible includes: country, season, seasons.
            ***See Sportmonks.com for information regarding includes.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    if league_id:
        log.info("Return a league by id: %s, with includes = %s", league_id, includes)
        return get_data(endpoint=f"leagues/{league_id}", includes=includes)
    else:
        log.info("Return all leagues")
        leagues = get_data(endpoint="leagues", includes=includes)
        log.info("Returned %s leagues with includes = %s", len(leagues), includes)
        return leagues


def get_seasons(season_id: int = None, includes: str = None):
    """
    Responses of the Seasons endpoint are limited to Seasons of the Leagues available in the
    Plan you are subscribed to.
    Responses provide you details about for example the Season ID, Name, League ID, Year and
    if the Season is Active Yes or No.
    If no season id is specified, all seasons will be returned

    Possible includes: league, stages, rounds, upcoming, results, groups, goalscorers, cardscorers,
    assistscorers, aggregatedGoalscorers, aggregatedCardscorers, aggregatedAssistscorers, fixtures
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
        return get_data(endpoint=f"seasons/{season_id}", includes=includes)
    else:
        log.info("Returning seasons")
        seasons = get_data(endpoint="seasons", includes=includes)
        log.info("Returned %s seasons, with includes = %s", len(seasons), includes)
        return seasons


def get_bookmakers(bookmaker_id: int = None):
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
        return get_data(endpoint=f"bookmakers/{bookmaker_id}")
    else:
        log.info("Returning all bookmakers")
        return get_data(endpoint="bookmakers")

def get_markets(market_id: int = None):
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
        return get_data(endpoint=f"markets/{market_id}")
    else:
        markets = get_data(endpoint="markets")
        log.info("Returning all markets; %s markets", len(markets))
        return markets


def get_fixtures_by_ids(fixture_ids: Union[int, List[int]], markets: Union[int, List[int]] = None,
                        bookmakers: Union[int, List[int]] = None, includes: str = None):
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

    if isinstance(fixture_ids, list):
        log.info("Returning fixtures by ids: %s, with includes = %s, markets = %s, bookmakers = %s",
                 fixture_ids, includes, markets, bookmakers)
        fixture_ids = ",".join(list(map(str, fixture_ids)))
        return get_data(endpoint=f"fixtures/multi/{fixture_ids}", includes=includes, params=params)
    elif isinstance(fixture_ids, int):
        log.info("Returning fixture by id: %s, with includes = %s, markets = %s, bookmakers = %s",
                 fixture_ids, includes, markets, bookmakers)
        return get_data(endpoint=f"fixtures/{fixture_ids}", includes=includes, params=params)
    else:
        raise TypeError(f"Did not expect fixture_ids of type: {type(fixture_ids)}")


def get_fixtures_by_date(date: str, league_ids: Union[int, List[int]] = None,
                         markets: Union[int, List[int]] = None,
                         bookmakers: Union[int, List[int]] = None,
                         includes: str = None):
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
    log.info("Returning fixtures by date %s, with includes = %s, league_ids = %s, markets = %s, \
             bookmakers = %s", date, includes, league_ids, markets, bookmakers)
    params = {"leagues": league_ids, "markets": markets, "bookmakers": bookmakers}
    return get_data(endpoint=f"fixtures/date/{date}", includes=includes, params=params)


def get_fixtures_in_date_range(start_date: str, end_date: str, team_id: int = None,
                               league_ids: Union[int, List[int]] = None,
                               markets: Union[int, List[int]] = None,
                               bookmakers: Union[int, List[int]] = None,
                               includes: str = None):

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
        log.info("Returning fixtures between %s and %s for team %s, with includes = %s, \
                 league_ids = %s,markets = %s, bookmakers = %s",
                 start_date, end_date, team_id, includes, league_ids, markets, bookmakers)
        return get_data(endpoint=f"fixtures/between/{start_date}/{end_date}/{team_id}",
                        includes=includes, params=params)
    else:
        log.info("Returning fixtures between %s and %s, with includes = %s, league_ids = %s, \
                 markets = %s, bookmakers = %s",
                 start_date, end_date, includes, league_ids, markets, bookmakers)
        return get_data(endpoint=f"fixtures/between/{start_date}/{end_date}", includes=includes,
                        params=params)


def get_fixtures_today(markets: Union[int, List[int]] = None,
                       bookmakers: Union[int, List[int]] = None,
                       league_ids: Union[int, List[int]] = None,
                       includes: str = None):

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
    fixtures_today = get_data(endpoint="livescores", includes=includes, params=params)
    log.info("Returning schedule for the current day: %s games,  params = %s, includes = %s",
             len(fixtures_today), params, includes)
    return fixtures_today

def get_inplay_fixtures(markets: Union[int, List[int]] = None,
                        bookmakers: Union[int, List[int]] = None,
                        league_ids: Union[int, List[int]] = None,
                        includes: str = None):

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
    log.info("Returning in play matches, params = %s, includes = %s",
             params, includes)
    return get_data(endpoint="livescores/now", includes=includes, params=params)

def get_head_to_head(team1_id: int, team2_id: int, includes: str = None):
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
    log.info("Returning head to head games between team %s and team %s with includes = %s",
             team1_id, team2_id, includes)
    return get_data(endpoint=f"head2head/{team1_id}/{team2_id}", includes=includes)

def get_standings(season_id: int, includes: str = None,
                  group_ids: Union[int, List[int]] = None,
                  stage_ids: Union[int, List[int]] = None):

    """
    Standings represent the rankings of Teams in the different Leagues they participate.
    Responses of the Standings endpoint can be returned in 2 formats, depending on the League setup.
    For ‘normal’ Leagues the response format is different compared to Cups.

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
    log.info("Returning standings for season %s with includes = %s, group_ids = %s, stage_ids = %s",
             season_id, includes, group_ids, stage_ids)
    params = {"stage_ids": stage_ids, "group_ids": group_ids}
    return get_data(endpoint=f"standings/season/{season_id}", includes=includes, params=params)

def get_standings_by_season_and_round_id(season_id: int, round_id: int):
    """
    Standings represent the rankings of Teams in the different Leagues they participate.
    With this endpoint you are able to retreive the standings for a given round.
    It will calculate the games played up until the given round id
    and provide a standings result for it.
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT


    Args:
        season_id:
            id of the season you want to return standings for.
        round_id:
            id of the round you want to return standings for.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning standings for season id: %s and round id: %s",
             season_id, round_id)
    return get_data(endpoint=f"standings/season/{season_id}/round/{round_id}")

def get_standings_by_season_and_date(season_id: int, date: str):
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
    log.info("Returning standings by season %s and datetime %s", season_id, date)
    return get_data(endpoint=f"standings/season/{season_id}/date/{date}")

def get_team_by_id(team_id: int, includes: str = None):
    """
    With the Teams endpoint you can find all Team Details you need.
    You can think of information about when the Team is founded, Logo, Team Name, Short Name etc.

    Args:
        team_id:
            id of the team you want to return.
        includes: optional
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
    log.info("Returning team by id: %s with includes = %s", team_id, includes)
    return get_data(endpoint=f"teams/{team_id}", includes=includes)


def get_teams_played_in_season(season_id: int, includes: str = None):
    """
    Get all teams played in a season.

    Args:
        season_id:
            id of the season you want teams returning.
        includes: optional
            Possible includes: country, squad, coach, transfers, sidelined, stats,
            venue, fifaranking,uefaranking, visitorFixtures, localFixtures,
            visitorResults, latest, upcoming, country,
            goalscorers,cardscorers, assistscorers, aggregatedGoalscorers,
            aggregatedCardscorers, aggregatedAssistscorers,
            league, activeSeasons, trophies.
            ***See Sportmonks.com for information regarding includes.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning all teams played in season %s with includes = %s",
             season_id, includes)
    return get_data(endpoint=f"teams/season/{season_id}", includes=includes)

def get_team_by_name(criteria: str, includes: str = None):
    """
    Get teams by criteria. For example, "United" will return all teams with "United" in
    their name.

    Args:
        criteria:
            Criteria to search by.
        includes: optional
            Possible includes: country, squad, coach, transfers, sidelined,
            stats, venue, fifaranking,uefaranking, visitorFixtures, localFixtures,
             visitorResults, latest, upcoming, country,
            goalscorers,cardscorers, assistscorers, aggregatedGoalscorers,
            aggregatedCardscorers, aggregatedAssistscorers, league,
            activeSeasons, trophies.
            ***See Sportmonks.com for information regarding includes.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning team: %s with includes = %s", criteria, includes)
    return get_data(endpoint=f"teams/search/{criteria}")


def get_current_leagues_for_team(team_id: int, date_range: List[str] = None):
    """
    Return all the current leagues a given team participates in
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

    Args:
        team_id:
            id of the team you want current leagues for.
        date_range: optional
            Range of dates you want the leagues for.
            YYYY-MM-DD format.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning all competitions for team %s in date range: %s",
             team_id, date_range)
    if date_range:
        date_range = ",".join(date_range)
    params = {"range": date_range}
    return get_data(endpoint=f"teams/{team_id}/current", params=params)

def get_all_leagues_for_team(team_id: int):
    """
    Return all the leagues/season a team ever participated in.
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

    Args:
        team_id:
            id of the team you want leagues returning for.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """

    log.info("Returning all competitions team %s have ever participated in.",
             team_id)
    return get_data(endpoint=f"teams/{team_id}/history")

def get_player_by_id(player_id: int, includes: str = None):
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
    log.info("Returning player %s with includes = %s", player_id, includes)
    return get_data(endpoint=f"players/{player_id}", includes=includes)



def get_player_by_name(criteria: str, includes: str = None):
    """
    This endpoint returns an array of Players that meet your search criteria.
    The Players endpoint provides you detailed Player information.
    With this endpoint you will be able to build a complete Player Profile.

    Args:
        criteria:
            Search players by criteria.
        includes: optional
            Possible includes: position, team, stats, trophies, sidelined, transfers,
            lineups, country
            ***See Sportmonks.com for information regarding includes.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning players matching search criteria: %s with includes = %s",
             criteria, includes)
    return get_data(endpoint=f"players/search/{criteria}", includes=includes)

def get_topscorers_by_season(season_id: int, stage_ids: Union[int, List[int]] = None,
                             includes: str = None):
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
    log.info("Returning topscorers at stages in a season %s with includes = %s, \
             stage_ids = %s", season_id, includes, stage_ids)
    params = {"stage_ids": stage_ids}
    return get_data(endpoint=f"topscorers/season/{season_id}", params=params,
                    includes=includes)

def get_aggregated_topscoreres_by_season(season_id: int, includes: str = None):
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
    log.info("Returning aggregated top scorers by season %s with includes = %s",
             season_id, includes)
    return get_data(endpoint=f"topscorers/season/{season_id}/aggregated", includes=includes)

def get_venue_by_id(venue_id: int):
    """
    The Venue endpoint provides Venue information like Name, City,
    Capacity, Address and even a Venue image.
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

    Args:
        venue_id:
            id of the venue you want to return.

    Response:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning venue %s", venue_id)
    return get_data(endpoint=f"venues/{venue_id}")

def get_venue_by_season_id(season_id: int):
    """
    Venues by season id.
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

    Args:
        season_id:
            id of the season you want venues returning for.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning venues by season id: %s", season_id)
    return get_data(endpoint=f"venues/season/{season_id}")

def get_round_by_id(round_id: int, includes: str = None):
    """
    Leagues can be split up in Rounds representing a week a game is played in.
    With this endpoint we give you the ability to request data for a single
    Round as well as all Rounds of a Season. The endpoint is often used in combination with includes
    like Results or Fixtures to show them based on Rounds.

    Args:
        round_id:
            id of the round you want returning.
        includes: optional
            Possible includes: fixtures, results, season, league.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning round by id %s with includes = %s", round_id, includes)
    return get_data(endpoint=f"round/{round_id}", includes=includes)

def get_rounds_by_season_id(season_id: int, includes: str = None):
    """
    Rounds by a given season id

    Args:
        season_id:
            id of the season you want the rounds for.
        includes: optional
            Possible includes: fixtures, results, season, league

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning rounds by season id: %s with includes %s", season_id, includes)
    return get_data(endpoint=f"rounds/season/{season_id}", includes=includes)

def get_odds_by_fixture_and_bookmaker(fixture_id: int, bookmaker_id: int):
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

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning odds by fixture: %s and bookmaker: %s", fixture_id, bookmaker_id)
    return get_data(endpoint=f"odds/fixture/{fixture_id}/bookmaker/{bookmaker_id}")

def get_odds_by_fixture_and_market(fixture_id: int, market_id: int):
    """
    Odds for specified fixture and market.
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT.

    Args:
        fixture_id:
            id of the fixture you want odds returning for.
        market_id:
            id of the market you want odds returning for.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning odds for market %s for fixture %s", market_id, fixture_id)
    return get_data(endpoint=f"odds/fixture/{fixture_id}/market/{market_id}")

def get_odds_by_fixture_id(fixture_id: int):
    """
    Odds by fixture
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

    Args:
        fixture_id:
            id of the fixture you want odds data for.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning odds by fixture: %s", fixture_id)
    return get_data(endpoint=f"odds/fixture/{fixture_id}")

def get_live_odds_by_fixture(fixture_id: int):
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
    log.info("Returning live odds for fixture %s", fixture_id)
    return get_data(endpoint=f"odds/inplay/fixture/{fixture_id}")

def get_coach_by_id(coach_id: int):
    """
    The Coaches endpoint provides you details about the Coach like its Name,
    Nationality Birthdate etc. By default this endpoint returns Coach details that have hosted at
    least 1 game under the Leagues covered by the Plan you are subscribed to.
    ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

    Args:
        coach_id:
            id of the coach you want to return.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning coach by coach_id: %s", coach_id)
    return get_data(endpoint=f"coaches/{coach_id}")

def get_stage_by_id(stage_id: int, includes: str = None):
    """
    Leagues and Seasons all over the world can have a different set up.
    The Stages endpoint can help you to define the current
    Stage or set up of multiple Stages of a particular League/Season.
    Stages names are for example: Regular Season, Play-offs, Semi-Finals, Final etc.

    Args:
        stage_id:
            id of the stage you want to return info from.
        includes: optional
            Possible includes: fixtures, results, season, league

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning stage by id: %s", stage_id)
    return get_data(endpoint=f"stages/{stage_id}", includes=includes)

def get_stages_by_season(season_id: int, includes: str = None):
    """
    Stages by season id.

    Args:
        season_id:
            id of the season you want to return stages for.
        includes: optional
            Possible includes: fixtures, results, season, league.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.

    """
    log.info("Returning stages in season %s", season_id)
    return get_data(endpoint=f"stages/season/{season_id}", includes=includes)

def get_squads(season_id: int, team_id: int, includes: str = None):
    """
    Since November 2017 we offer the ability to load historical Squads.
    This means you can retrieve Squads from 2005 onwards,
    including Player performance of those Games of the requested Season.

    The squad include on any team related endpoint or include will only return the
    squad of the current season of the domestic league the team is playing in.
    You can use this endpoint to load squads for a different season or even for cups.

    Args:
        season_id:
            id of the season you want to return squads for.
        team_id:
            id of the team you want squads returning.
        includes: optional
            Possible includes: player

    """
    log.info("Returning squad for team %s during season %s", team_id, season_id)
    return get_data(endpoint=f"squad/season/{season_id}/team/{team_id}", includes=includes)
