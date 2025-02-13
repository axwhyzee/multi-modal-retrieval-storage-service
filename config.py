import os


def get_aws_bucket_name() -> str:
    return os.environ["AWS_S3_BUCKET_NAME"]
