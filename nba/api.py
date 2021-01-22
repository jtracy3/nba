import requests
from nba.constants import BOXSCORE, PLAYERS, SCHEDULE, TEAMS
from nba.base.models import (
    BoxscoreRecord, PlayerYearRecord, ScheduleRecord,
    TeamRecord
)
from hashlib import md5
from typing import List


class NBAApi:

    _URL = 'http://data.nba.net/data/10s/'

    @staticmethod
    def _clean_response(endpoint: str, key_map: List[str], values: List[str] = None):

        response = requests.get(endpoint)
        response_json = response.json()

        try:
            for key in key_map:
                response_json = response_json[key]
        except KeyError:
            raise KeyError

        output = list()
        for data in response_json:
            if values is not None:
                output.append({data_key: data[data_key] for data_key in values if data_key in data})
            else:
                output.append(data)

        return output

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

    @staticmethod
    def _records(response, game_id, game_date):
        """
        Turns the json response into a list of `Records` to enforce data types.
        `Records` are of the `DataClassBase` type.

        Args:
            response: json response
            game_id: game id
            game_date: game data format 'YYYYMMDD'-'%Y%m%d'
        Return:
            data: list of BoxscoreRecords
        """
        data = []
        for dict_ in response:
            key = md5((dict_['personId'] + game_id).encode()).hexdigest()
            data.append(BoxscoreRecord(**dict(dict_, boxscoreId=key, gameId=game_id, gameDate=game_date)))

        return data

    def get(self, game_date: str, game_id: str):
        """
        GET response from boxscore endpoint

        Args:
            game_date (str): game date
            game_id (str): game_id
        Return:
            List of `BoxscoreRecord`s
        """

        endpoint = self._URL + f'prod/v1/{game_date}/{game_id}_boxscore.json'
        r_json = requests.get(endpoint, timeout=120).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=BOXSCORE) for r in r_json]

        return self._records(r_json, game_id, game_date)


# TODO: add players info
class Players(NBAApi):

    key = 'standard'

    @staticmethod
    def _records(response, season):
        """
        Turns the json response into a list of `Records` to enforce data types.
        `Records` are of the `DataClassBase` type.

        Args:
            response: json response
            season: season
        Return:
            data: list of PlayerRecords
        """
        data = []
        for dict_ in response:
            key = md5((dict_['personId'] + str(season)).encode()).hexdigest()
            data.append(PlayerYearRecord(**dict(dict_, playerYearId=key, seasonId=season)))

        return data

    def get(self, season: int):
        """
        GET response from players endpoint

        Args:
            season (int): season
        Return:
            List of `PlayerYearRecord`s
        """

        endpoint = self._URL + f'prod/v1/{season}/players.json'
        r_json = requests.get(endpoint).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=PLAYERS) for r in r_json]
        r_json = list(filter(lambda x: x['teamId'] != '', r_json))

        return self._records(r_json, season)


class Schedule(NBAApi):

    key = 'standard'

    @staticmethod
    def _records(response, season):
        """
        Turns the json response into a list of `Records` to enforce data types.
        `Records` are of the `DataClassBase` type.

        Args:
            response: json response
            season: season
        Return:
            data: list of PlayerRecords
        """
        data = []
        for dict_ in response:
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
            data.append(ScheduleRecord(**dat))

        return data

    def get(self, season: int):
        """
        GET response from players endpoint

        Args:
            season (int): season
        Return:
            List of `ScheduleRecord`s
        """

        endpoint = self._URL + f'prod/v1/{season}/schedule.json'
        r_json = requests.get(endpoint).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=SCHEDULE) for r in r_json]

        return self._records(r_json, season)


class Teams(NBAApi):

    key = 'standard'

    @staticmethod
    def _records(response, season):
        """
        Turns the json response into a list of `Records` to enforce data types.
        `Records` are of the `DataClassBase` type.

        Args:
            response: json response
            season: season
        Return:
            data: list of TeamRecords
        """
        data = []
        for dict_ in response:
            dict_.pop('isNBAFranchise')
            dict_['seasonId'] = season
            data.append(TeamRecord(**dict_))

        return data

    def get(self, season: int):
        """
        GET response from players endpoint

        Args:
            season (int): season
        Return:
            List of `PlayerYearRecord`s
        """

        endpoint = self._URL + f'prod/v2/{season}/teams.json'
        r_json = requests.get(endpoint).json()

        # Because extract creates a generator we need to turn it into a list
        r_json = list(self.extract(r_json, self.key))[0]
        r_json = [self._filter_response(r, values=TEAMS) for r in r_json]
        r_json = list(filter(lambda x: x['isNBAFranchise'], r_json))

        return self._records(r_json, season)
