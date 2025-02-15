import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv


def get_aws_bucket_name() -> str:
    return os.environ["AWS_S3_BUCKET_NAME"]


def _initialize_aws_creds():
    AWS_CREDS_FILE_PATH = os.path.expanduser("~/.aws/credentials")
    creds_file_path = Path(AWS_CREDS_FILE_PATH)
    creds_file_path.parent.mkdir(exist_ok=True, parents=True)
    creds_file_path.write_text(
        f"[default]\n"
        f'aws_access_key_id = {os.environ["AWS_S3_BUCKET_ACCESS_KEY"]}\n'
        f'aws_secret_access_key = {os.environ["AWS_S3_BUCKET_SECRET_ACCESS_KEY"]}\n'
        f'region = {os.environ["AWS_S3_BUCKET_REGION"]}'
    )


def bootstrap():
    load_dotenv(find_dotenv())
    _initialize_aws_creds()
