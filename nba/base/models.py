from dataclasses import dataclass, fields, asdict
import datetime as dt
import abc


@dataclass
class DataClassBase:

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                value = 0 if not value else value
                setattr(self, field.name, field.type(value))

    @abc.abstractmethod
    def keys(self):
        """Returns dataclass keys (fields)"""

    @abc.abstractmethod
    def asdict(self):
        """Returns dataclass as dictionary"""


# TODO: consider changing this to include a list. A boxscore record contains many players
@dataclass
class BoxscoreRecord(DataClassBase):
    boxscoreId: str = None
    gameId: str = None
    personId: str = None
    teamId: str = None
    gameDate: str = None
    points: int = None
    pos: str = None
    min: str = None
    fgm: int = None
    fga: int = None
    fgp: float = None
    ftm: int = None
    fta: int = None
    ftp: float = None
    tpm: int = None
    tpa: int = None
    tpp: float = None
    offReb: int = None
    defReb: int = None
    totReb: int = None
    assists: int = None
    pFouls: int = None
    steals: int = None
    turnovers: int = None
    blocks: int = None
    plusMinus: int = None
    dnp: str = None

    def keys(self):
        return [field.name for field in fields(self)]

    def asdict(self):
        return asdict(self)


@dataclass
class PlayerYearRecord(DataClassBase):
    playerYearId: str = None
    personId: str = None
    teamId: str = None
    seasonId: int = None
    firstName: str = None
    lastName: str = None
    temporaryDisplayName: str = None
    heightFeet: int = None
    heightInches: int = None
    heightMeters: float = None
    weightPounds: int = None
    weightKilograms: float = None
    pos: str = None
    nbaDebutYear: int = None
    collegeName: str = None
    yearsPro: str = None
    # draft_round_number: int
    # draft_pick_number: int
    # draft_year: int
    # draft_team_id: int
    dateOfBirthUTC: str = None

    def keys(self):
        return [field.name for field in fields(self)]

    def asdict(self):
        return asdict(self)
