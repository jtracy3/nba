import boto3
from io import StringIO
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET = os.getenv('BUCKET')
REGION_NAME = os.getenv('REGION_NAME')
AWS_PROFILE = os.getenv('AWS_PROFILE')


def to_s3(data, date):
    """
    Send data to s3

    Args:
    ----
        data (pd.DataFrame): data from nba api
    Returns:
    -------
        None
    """

    csv_buffer = StringIO()
    # Write dataframe to buffer
    data.to_csv(csv_buffer, index=False)
    filename = date + '_boxscore_data.csv'

    # Create S3 object
    s3_resource = boto3.resource("s3")
    # Write buffer to S3 object
    s3_resource.Object(BUCKET, filename).put(Body=csv_buffer.getvalue())

    print(f'File - {filename} successfully dumped into {BUCKET} - {date}')
