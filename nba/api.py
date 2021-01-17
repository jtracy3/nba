import requests
from typing import List
from api.constants import *


class NBAApi:

    URL = 'http://data.nba.net/data/10s/'

    def schedule(self, season: int) -> List[dict]:

        endpoint = self.URL + f'prod/v1/{season}/schedule.json'
        keys = ['league', 'standard']
        schedule = self._clean_response(endpoint=endpoint, key_map=keys, values=SCHEDULE)

        return schedule

    # I might have everything I need above
    def scoreboard(self, game_date: str) -> List[dict]:

        endpoint = self.URL + f'prod/v2/{game_date}/scoreboard.json'
        keys = ['games']
        scoreboard = self._clean_response(endpoint=endpoint, key_map=keys, values=SCOREBOARD)

        return scoreboard

    def boxscore(self, game_date: str, game_id: str) -> List[dict]:

        endpoint = self.URL + f'prod/v1/{game_date}/{game_id}_boxscore.json'
        keys = ['stats', 'activePlayers']
        stats = self._clean_response(endpoint=endpoint, key_map=keys, values=BOXSCORE)

        return [dict(item, gameId=game_id) for item in stats]

    def players(self, season: int) -> List[dict]:

        endpoint = self.URL + f'prod/v1/{season}/players.json'
        keys = ['league', 'standard']
        players = self._clean_response(endpoint=endpoint, key_map=keys, values=PLAYERS)

        return [dict(item, seasonId=season) for item in players]

    # TODO: add this
    def teams(self, season):
        endpoint = self.URL + f'prod/v1/{season}/teams.json'
        keys = ['league', 'standard']
        teams = self._clean_response(endpoint=endpoint, key_map=keys, values=TEAMS)

        return [dict(item, seasonId=season) for item in teams]

    @staticmethod
    def _clean_response(endpoint, key_map, values=None):
        response = requests.get(endpoint)
        response_json = response.json()

        try:
            for key in key_map:
                response_json = response_json[key]
        except KeyError:
            # could probably handle this better
            pass

        output = list()
        for data in response_json:
            if values is not None:
                output.append({data_key: data[data_key] for data_key in values if data_key in data})
            else:
                output.append(data)

        return output