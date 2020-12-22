from api.nba_api import NBAApi
from src.utils import to_s3
import datetime as dt
import pandas as pd


def main():
    # session = boto3.session.Session(region_name=REGION_NAME, profile_name=AWS_PROFILE)

    # date yesterday
    str_date = (dt.date.today() - dt.timedelta(days=1)).strftime('%Y%m%d')

    nba = NBAApi()
    game_ids = nba.get_gameids(str_date)

    boxscore_full = pd.DataFrame()
    for game_id in game_ids:
        boxscore = nba.boxscore_df(game_date=str_date, game_id=game_id)
        boxscore_full = boxscore_full.append(boxscore)

    print('Sending data to S3')
    to_s3(boxscore_full, str_date)


if __name__ == '__main__':
    main()
