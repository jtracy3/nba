"""
Contains all the fields we want from API calls
"""

SCHEDULE = [
    "gameId",
    "seasonStageId",
    "startTimeUTC",
    "startDateEastern",
    "nugget",
    "hTeam",
    "vTeam"
]

SCOREBOARD = [
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

TEAMS = [
    "isNBAFranchise",
    "isAllStar",
    "city",
    "altCityName",
    "fullName",
    "tricode",
    "teamId",
    "nickname",
    "teamShortName",
    "confName",
    "divName"
]

BOXSCORE = [
    "personId",
    "teamId",
    "points",
    "pos",
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

PLAYERS = [
    "firstName",
    "lastName",
    "temporaryDisplayName",
    "personId",
    'teamId',
    "pos",
    "heightFeet",
    "heightInches",
    "heightMeters",
    "weightPounds",
    "weightKilograms",
    "dateOfBirthUTC",
    "nbaDebutYear",
    "yearsPro",
    "collegeName",
]