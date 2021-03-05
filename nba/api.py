import requests
from nba.constants import BOXSCORE, PLAYERS, SCHEDULE, TEAMS, SCOREBOARD
from hashlib import md5
from typing import List
from collections import OrderedDict


class NBAApi:

    _URL = 'http://data.nba.net/data/10s/'

    def extract(self, json, key):
        """
        Creates a generator containing the data in the given `key`

        Args:
            json: json response
            key: response key of interest
        Returns:
            Generator containing the data for the given object key
        """
        if isinstance(json, dict):
            for k, v in json.items():
                if k == key:
                    yield v
                else:
                    yield from self.extract(v, key)
        elif isinstance(json, list):
            for item in json:
                yield from self.extract(item, key)

    @staticmethod
    def _filter_response(response, values):
        # Could probably add a try except for if values is None
        if values is None:
            return response
        return {key: response[key] for key in values if key in response}


class Boxscore(NBAApi):

    key = 'activePlayers'

    def get(self, game_date: str, game_id: str):
        """
        GET response from boxscore endpoint

        Args:
            game_date (str): game date
            game_id (str): game_id
        Return:
            List of boxscore dictionaries
        """

        endpoint = self._URL + f'prod/v1/{game_date}/{game_id}_boxscore.json'
        r_json = requests.get(endpoint, timeout=120).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=BOXSCORE) for r in r_json]

        boxscore = []
        for dict_ in r_json:
            key = md5((dict_['personId'] + game_id).encode()).hexdigest()
            boxscore.append(dict(dict_, gameId=game_id, gameDate=game_date, boxscoreId=key))

        return boxscore


# TODO: add players info
class Players(NBAApi):

    key = 'standard'

    def get(self, season: int):
        """
        GET response from players endpoint

        Args:
            season (int): season
        Return:
            List of player dictionaries
        """

        endpoint = self._URL + f'prod/v1/{season}/players.json'
        r_json = requests.get(endpoint).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=PLAYERS) for r in r_json]
        r_json = list(filter(lambda x: x['teamId'] != '', r_json))

        players = []
        for dict_ in r_json:
            dict_.pop('teamId')
            players.append(dict_)

        return


class Schedule(NBAApi):

    key = 'standard'

    def get(self, season: int):
        """
        GET response from schedule endpoint

        Args:
            season (int): season
        Return:
            List of schedule dictionaries
        """

        endpoint = self._URL + f'prod/v1/{season}/schedule.json'
        r_json = requests.get(endpoint).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=SCHEDULE) for r in r_json]

        schedules = []
        for dict_ in r_json:
            dat = {
                'gameId': dict_['gameId'],
                'seasonId': season,
                'seasonStageId': dict_['seasonStageId'],
                'startTimeUTC': dict_['startTimeUTC'],
                'startDateEastern': dict_['startDateEastern'],
                'nugget': dict_['nugget']['text'],
                'hTeamId': dict_['hTeam']['teamId'],
                'vTeamId': dict_['vTeam']['teamId']
            }
            schedules.append(dat)

        return schedules


class Teams(NBAApi):

    key = 'standard'

    def get(self, season: int):
        """
        GET response from teams endpoint

        Args:
            season (int): season
        Return:
            List of team dictionaries
        """

        endpoint = self._URL + f'prod/v2/{season}/teams.json'
        r_json = requests.get(endpoint).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=TEAMS) for r in r_json]
        r_json = list(filter(lambda x: x['isNBAFranchise'], r_json))

        teams = []
        for dict_ in r_json:
            dict_.pop('isNBAFranchise')
            dict_['seasonId'] = season
            teams.append(dict_)

        return teams


class Scoreboard(NBAApi):

    key = 'games'

    def get(self, game_date: str):
        """
        GET response from scoreboard endpoint

        Args:
            game_date (int): season
        Return:
            List of scoreboard dictionaries
        """

        endpoint = self._URL + f'prod/v2/{game_date}/scoreboard.json'
        r_json = requests.get(endpoint).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=SCOREBOARD) for r in r_json]

        scoreboard = []
        for dict_ in r_json:
            dat = {
                'gameId': dict_['gameId'],
                'seasonId': dict_['seasonYear'],
                'seasonStageId': dict_['seasonStageId'],
                'leagueName': dict_['leagueName'],
                'startTimeUTC': dict_['startTimeUTC'],
                #'endTimeUTC': dict_['endTimeUTC'],
                'startDateEastern': dict_['startDateEastern'],
                'nugget': dict_['nugget']['text'],
                'attendance': dict_['attendance'],
                'hTeamId': dict_['hTeam']['teamId'],
                'vTeamId': dict_['vTeam']['teamId']
            }
            scoreboard.append(dat)

        return scoreboard
