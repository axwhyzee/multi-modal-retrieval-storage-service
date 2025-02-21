import logging
from abc import ABC, abstractmethod
from pathlib import Path

import boto3  # type: ignore

from config import get_aws_connection_params, get_aws_s3_bucket_name

logger = logging.getLogger(__name__)


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, data: bytes, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError


class S3Repository(AbstractRepository):
    def __init__(self):
        self._bucket_name = get_aws_s3_bucket_name()
        self._client = boto3.client("s3", **get_aws_connection_params())

    def add(self, data: bytes, key: str) -> None:
        self._client.put_object(Bucket=self._bucket_name, Key=key, Body=data)

    def delete(self, key: str) -> None:
        self._client.delete_object(Bucket=self._bucket_name, Key=key)

    def get(self, key: str) -> bytes:
        response = self._client.get_object(Bucket=self._bucket_name, Key=key)
        return response["Body"].read()


class LocalRepository(AbstractRepository):
    """For testing without consumption of S3 resources"""

    def __init__(self):
        self._upload_folder = Path("uploads")
        self._upload_folder.mkdir(exist_ok=True)

    def add(self, data: bytes, key: str) -> None:
        local_path = self._upload_folder / key
        local_path.parent.mkdir(exist_ok=True)
        local_path.write_bytes(data)

    def delete(self, key: str) -> None:
        local_path = self._upload_folder / key
        local_path.unlink(missing_ok=True)

    def get(self, key: str) -> bytes:
        local_path = self._upload_folder / key
        return local_path.read_bytes()
