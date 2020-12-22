import requests
from typing import List


class NBAApi:

    URL = 'http://data.nba.net/data/10s/'

    def schedule(self, season: int) -> List[dict]:

        SCHEDULE_COLS = [
            "gameId",
            "seasonStageId",
            "startTimeUTC",
            "startDateEastern",
            "nugget",
            "hTeam",
            "vTeam"
        ]

        endpoint = self.URL + f'prod/v1/{season}/schedule.json'
        keys = ['league', 'standard']
        schedule = self._clean_response(endpoint=endpoint, key_map=keys, values=SCHEDULE_COLS)

        return schedule

    # I might have everything I need above
    def scoreboard(self, game_date: str) -> List[dict]:

        SCOREBOARD_COL = [
            "seasonStageId",
            "seasonYear",
            "leagueName",
            "gameId",
            "startTimeEastern",
            "startTimeUTC",
            "endTimeUTC",
            "startDateEastern",
            "nugget",
            "attendance",
            "vTeam",
            "hTeam"
        ]

        endpoint = self.URL + f'prod/v2/{game_date}/scoreboard.json'
        keys = ['games']
        scoreboard = self._clean_response(endpoint=endpoint, key_map=keys, values=SCOREBOARD_COL)

        return scoreboard

    def boxscore(self, game_date: str, game_id: str) -> List[dict]:

        BOXSCORE_COLS = [
            "personId",
            "firstName",
            "lastName",
            "jersey",
            "teamId",
            "points",
            "pos",
            "position_full",
            "player_code",
            "min",
            "fgm",
            "fga",
            "fgp",
            "ftm",
            "fta",
            "ftp",
            "tpm",
            "tpa",
            "tpp",
            "offReb",
            "defReb",
            "totReb",
            "assists",
            "pFouls",
            "steals",
            "turnovers",
            "blocks",
            "plusMinus",
            "dnp"
        ]

        endpoint = self.URL + f'prod/v1/{game_date}/{game_id}_boxscore.json'
        keys = ['stats', 'activePlayers']
        stats = self._clean_response(endpoint=endpoint, key_map=keys, values=BOXSCORE_COLS)

        return stats

    def players(self, season: int) -> List[dict]:

        PLAYERS_COLS = [
            "firstName",
            "lastName",
            "temporaryDisplayName",
            "personId",
            "teamId",
            "jersey",
            "isActive",
            "pos",
            "heightFeet",
            "heightInches",
            "heightMeters",
            "weightPounds",
            "weightKilograms",
            "dateOfBirthUTC",
            "teams",
            "nbaDebutYear",
            "yearsPro",
            "collegeName",
            "lastAffiliation",
            "country"
        ]

        endpoint = self.URL + f'prod/v1/{season}/players.json'
        keys = ['league', 'standard']
        players = self._clean_response(endpoint=endpoint, key_map=keys, values=PLAYERS_COLS)

        return players

    # TODO: add this
    def teams(self, season):
        pass

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
                r_dict = dict()
                for data_key in values:
                    if data_key not in data.keys():
                        r_dict[data_key] = None
                    else:
                        r_dict[data_key] = data[data_key]
                output.append(r_dict)
            else:
                output.append(data)

        return output

# output.append({data_key: data[data_key] for data_key in values})