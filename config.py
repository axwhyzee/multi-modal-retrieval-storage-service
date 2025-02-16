import os
from typing import Any, Dict, TypeAlias

Config: TypeAlias = Dict[str, Any]


def get_aws_s3_bucket_name() -> str:
    return os.environ["AWS_S3_BUCKET_NAME"]


def get_redis_connection_params() -> Config:
    return {
        "host": os.environ["REDIS_HOST"],
        "port": os.environ["REDIS_PORT"],
        "username": os.environ["REDIS_USERNAME"],
        "password": os.environ["REDIS_PASSWORD"],
        "decode_responses": True,
    }


def get_aws_connection_params() -> Config:
    return {
        "aws_access_key_id": os.environ["AWS_S3_BUCKET_ACCESS_KEY"],
        "aws_secret_access_key": os.environ["AWS_S3_BUCKET_SECRET_ACCESS_KEY"],
        "region_name": os.environ["AWS_S3_BUCKET_REGION"],
    }
