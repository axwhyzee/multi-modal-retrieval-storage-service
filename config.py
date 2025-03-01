import os
from pathlib import Path
from typing import Any, Dict, TypeAlias

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

Config: TypeAlias = Dict[str, Any]


def get_aws_s3_bucket_name() -> str:
    return os.environ["AWS_S3_BUCKET_NAME"]


def get_aws_connection_params() -> Config:
    return {
        "aws_access_key_id": os.environ["AWS_S3_BUCKET_ACCESS_KEY"],
        "aws_secret_access_key": os.environ["AWS_S3_BUCKET_SECRET_ACCESS_KEY"],
        "region_name": os.environ["AWS_S3_BUCKET_REGION"],
    }


def get_local_repo_upload_folder() -> Path:
    return Path(".uploads")
