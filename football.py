"""SportMonks Football API"""

import os
import logging
from typing import Dict, Optional, Union, List, Any
from base import BaseAPI
import helper
from errors import IncompatibleArgs

log = helper.setup_logger(__name__, "SM_API.log")

class SportMonks(BaseAPI):
    """SportMonks API"""

    def __init__(self, api_key: str = None, timeout: Optional[int] = 2):
        super().__init__(api_key, timeout)

    def continents(self, continent_id: Optional[int] = None,
                   includes: Optional[Union[str, List[str]]] = None):
        """
        The Continents endpoint helps you with assigning Countries and Leagues
        to the part of the world (Continent) they belong to.
        Available Continents are Europe, Asia, Africa, Oceania,
        North America and South America.

        Args:
            continent_id:
                id of the continent you want to retrieve.
                If no continent_id is specified, all continents will be returned.
            includes:
                Possible includes: countries.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        if continent_id:
            log.info("Get continent by id: %s, with includes = %s", continent_id, includes)
            return self.make_request(endpoint=["continents", continent_id], includes=includes)
        else:
            log.info("Get all continents")
            continents = self.make_request(endpoint="continents", includes=includes)
            log.info("Returned %s continents with includes = %s", len(continents), includes)
            return continents

    def countries(self, country_id: Optional[int] = None,
                  includes: Optional[Union[str, List[str]]] = None):

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
            return self.make_request(endpoint=["countries", country_id], includes=includes)
        else:
            log.info("Returning all countries")
            countries = self.make_request(endpoint="countries", includes=includes)
            log.info("Returned %s countries with includes = %s", len(countries), includes)
            return countries

    def leagues(self, league_id: Optional[int] = None, search: Optional[str] = None,
                includes: Optional[Union[str, List[str]]] = None):

        """
        A request on this endpoint would return a response with all Leagues you have access to,
        based on the plan you are subscribed to. The Leagues endpoint provides you
        League information like its ID, Name, Country, Coverage etc.
        If no league id is specified, all leagues in your plan will be returned

        Args:
            league_id:
                id of the league you want to retrieve.
                If no league_id is specified, all leagues in your plan will be returned.
            search:
                Search for a league by name.
            includes:
                Possible includes: country, season, seasons.
                ***See Sportmonks.com for information regarding includes.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """
        if league_id:
            log.info("Return a league by id: %s, with includes = %s", league_id, includes)
            return self.make_request(endpoint=["leagues", league_id], includes=includes)
        elif search:
            log.info("Returning a league by search: %s", search)
            return self.make_request(endpoint=["leagues", "search", search], includes=includes)
        else:
            log.info("Returning all leagues")
            leagues = self.make_request(endpoint="leagues", includes=includes)
            log.info("Returned %s leagues with includes = %s", len(leagues), includes)
            return leagues

    def seasons(self, season_id: Optional[int] = None,
                includes: Optional[Union[str, List[str]]] = None):
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
            return self.make_request(endpoint=["seasons", season_id], includes=includes)
        else:
            log.info("Returning all seasons")
            seasons = self.make_request(endpoint="seasons", includes=includes)
            log.info("Returned %s seasons, with includes = %s", len(seasons), includes)
            return seasons

    def bookmakers(self, bookmaker_id: Optional[int] = None):
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
            return self.make_request(endpoint=["bookmakers", bookmaker_id])
        else:
            log.info("Returning all bookmakers")
            return self.make_request(endpoint="bookmakers")

    def markets(self, market_id: Optional[int] = None):
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
            return self.make_request(endpoint=["markets", market_id])
        else:
            markets = self.make_request(endpoint="markets")
            log.info("Returning all markets; %s markets", len(markets))
            return markets

    def teams(self, team_id: Optional[int] = None, season_id: Optional[int] = None,
              includes: Optional[Union[str, List[str]]] = None):

        """
        With the Teams endpoint you can find all Team Details you need.
        You can think of information about when the Team is founded, Logo, Team Name,
        Short Name etc.

        Args:
            team_id:
                id of the team you want to return.
            season_id:
                id of the season you want to return.
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

        if team_id and season_id:
            raise IncompatibleArgs("Can only supply one of: team_id, season_id.")

        if team_id:
            return self.make_request(endpoint=["teams", team_id], includes=includes)
        elif season_id:
            return self.make_request(endpoint=["teams", "season", season_id], includes=includes)
        else:
            # check what happens when nothing is supplied
            pass

    def team_current_leagues(self, team_id: int):
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
        return self.make_request(endpoint=["teams", team_id, "current"])

    def team_historic_leagues(self, team_id):
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

        return self.make_request(endpoint=["teams", team_id, "history"])


    def squads(self, season_id: int, team_id: int,
               includes: Optional[str, List[str]] = None):

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

        return self.make_request(endpoint=["squad", "season", season_id, "team", team_id],
                                 includes=includes)

    def commentaries(self, fixture_id: int):
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

        return self.make_request(endpoint=["commentaries", "fixture", fixture_id])

    def venues(self, venue_id: Optional[int] = None,
               season_id: Optional[int] = None):

        """
        The Venue endpoint provides Venue information like Name, City,
        Capacity, Address and even a Venue image.
        If venue_id supplied, then info will be returned for that venue.
        If season_id supplied, then all venues for that season will be returned.
        ***NO INCLUDES AVAILABLE FOR THIS ENDPOINT

        Args:
            venue_id:
                id of the venue you want to return.
            season_id:
                id of the season you want the venues for

        Response:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        if venue_id and season_id:
            raise IncompatibleArgs("Only one of season_id and venue_id can be supplied.")

        if venue_id:
            return self.make_request(endpoint=["venues", venue_id])
        elif season_id:
            return self.make_request(endpoint=["venues", "season", season_id])
        else:
            # check what happpens when nothing supplied
            pass

    def coaches(self, coach_id: int):

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
        return self.make_request(endpoint=["coaches", coach_id])

    def rounds(self, round_id: Optional[int] = None,
               season_id: Optional[int] = None,
               includes: Optional[str, List[str]] = None):

        """
        Leagues can be split up in Rounds representing a week a game is played in.
        With this endpoint we give you the ability to request data for a single
        Round as well as all Rounds of a Season. The endpoint is often used in
        combination with includeslike Results or Fixtures to show them based on Rounds.

        Args:
            round_id:
                id of the round you want returning.
            season_id:
                id of the season you want returning.
            includes:
                Possible includes: fixtures, results, season, league.

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.

        """

        if round_id and season_id:
            raise IncompatibleArgs("Cannot have both round_id and season_id.")

        if round_id:
            return self.make_request(endpoint=["round", round_id], includes=includes)
        elif season_id:
            return self.make_request(endpoint=["rounds", "season", season_id],
                                     includes=includes)

    def stages(self, stage_id: Optional[int] = None,
               season_id: Optional[int] = None,
               includes: Optional[str, List[str]] = None):

        """
        Leagues and Seasons all over the world can have a different set up.
        The Stages endpoint can help you to define the current
        Stage or set up of multiple Stages of a particular League/Season.
        Stages names are for example: Regular Season, Play-offs, Semi-Finals, Final etc.

        Args:
            stage_id:
                id of the stage you want to return info from.
            season_id:
                id of the season you want the stages for.
            includes:
                Possible includes: fixtures, results, season, league

        Returns:
            Parsed HTTP response from SportMonks API.
            JSON format.
        """
        if stage_id and season_id:
            raise IncompatibleArgs("Cannot supply stage_id and season_id.")

        if stage_id:
            return self.make_request(endpoint=["stages", stage_id], includes=includes)
        elif season_id:
            return self.make_request(endpoint=["stages", "season", season_id], includes=includes)
        else:
            # what happens when nothing is supplied
            pass

    def players(self, player_id: Optional[int] = None,
                search: Optional[str] = None,
                includes: Optional[str, List[str]] = None):
        """
        The Players endpoint provides you detailed Player information.
        With this endpoint you will be able to build a complete Player Profile.

        Args:
            player_id:
                id of the player.
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
        if player_id and search:
            raise IncompatibleArgs("Only one of player_id or search can be specified.")

        if player_id:
            return self.make_request(endpoint=["players", player_id], includes=includes)
        elif search:
            return self.make_request(endpoint=["players", "search", search], includes=includes)
        else:
            # what happens if nothing is supplied
            pass

    def fixtures(self, fixture_ids: Union[int, List[int]],
                 markets: Optional[Union[int, List[int]]] = None,
                 bookmakers: Optional[Union[int, List[int]]] = None,
                 includes: Optional[str, List[str]] = None):

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
            fixture_ids = ",".join(list(map(str, fixture_ids)))
            return self.make_request(endpoint=["fixtures", "multi", fixture_ids],
                                     includes=includes, params=params)
        else:
            return self.make_request(endpoint=["fixtures", fixture_ids],
                                     includes=includes, params=params)


    def fixtures_by_date(self, date: str, league_ids: Optional[Union[int, List[int]]] = None,
                         markets: Optional[Union[int, List[int]]] = None,
                         bookmakers: Optional[Union[int, List[int]]] = None,
                         includes: Optional[str, List[str]] = None):

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

        return self.make_request(endpoint=["fixtures", "date", date],
                                 includes=includes, params=params)

    def fixtures_in_data_range(self, start_date: str, end_date: str,
                               team_id: Optional[int] = None,
                               league_ids: Optional[Union[int, List[int]]] = None,
                               markets: Optional[Union[int, List[int]]] = None,
                               bookmakers: Optional[Union[int, List[int]]] = None,
                               includes: Optional[str, List[str]] = None):
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
            return self.make_request(endpoint=["fixtures", "between", start_date, end_date,
                                               team_id],
                                     includes=includes, params=params)
        else:
            return self.make_request(endpoint=["fixtures", "between", start_date, end_date],
                                     includes=includes, params=params)


    def inplay_fixtures(self, markets: Optional[Union[int, List[int]]] = None,
                        bookmakers: Optional[Union[int, List[int]]] = None,
                        league_ids: Optional[Union[int, List[int]]] = None,
                        includes: Optional[str, List[str]] = None):

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
        return self.make_request(endpoint=["livescores", "now"], includes=includes,
                                 params=params)


    def schedule_today(self, markets: Optional[Union[int, List[int]]] = None,
                       bookmakers: Optional[Union[int, List[int]]] = None,
                       league_ids: Optional[Union[int, List[int]]] = None,
                       includes: Optional[str, List[str]] = None):

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
        return self.make_request(endpoint="livescores", includes=includes, params=params)


    def head2head(self, team1_id: int, team2_id: int,
                  includes: Optional[str, List[str]] = None):

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
        return self.make_request(endpoint=["head2head", team1_id, team2_id], includes=includes)

    def standings(self, season_id: int, includes: Optional[str, List[str]] = None,
                  group_ids: Optional[Union[int, List[int]]] = None,
                  stage_ids: Optional[Union[int, List[int]]] = None):


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
        return self.make_request(endpoint=["standings", "season", season_id],
                                 includes=includes, params=params)

    def standings_by_date(self, season_id: int, date: str):
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
        return self.make_request(endpoint=["standings", "season", season_id, "date", date])

    def topscorers(self, season_id: int, stage_ids: Optional[Union[int, List[int]]] = None,
                   includes: Optional[str, List[str]] = None):

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
        return self.make_request(endpoint=["topscorers", "season", season_id],
                                 includes=includes, params=params)

    def aggregated_topscorers(self, season_id: int,
                              includes: Optional[str, List[str]] = None):

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
        return self.make_request(endpoint=["topscorers", "season", season_id, "aggregated"],
                                 includes=includes)


    def odds(self, fixture_id: int, bookmaker_id: Optional[int] = None,
             market_id: Optional[int] = None):

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
            return self.fixtures(fixture_ids=fixture_id, markets=market_id,
                                 bookmakers=bookmaker_id, includes="odds").get("odds")
        if bookmaker_id:
            return self.make_request(endpoint=["odds", "fixture", fixture_id,
                                               "bookmaker", bookmaker_id])
        if market_id:
            return self.make_request(endpoint=["odds", "fixture", fixture_id,
                                               "market", market_id])
        if not (bookmaker_id or market_id):
            return self.make_request(endpoint=["odds", "fixture", fixture_id])

    def live_odds(self, fixture_id: int):
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
        return self.make_request(endpoint=["odds", "inplay", "fixture", fixture_id])
