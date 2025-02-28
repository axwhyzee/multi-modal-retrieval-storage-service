import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

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

    def get(self, key: str) -> bytes:
        response = self._client.get_object(Bucket=self._bucket_name, Key=key)
        return response["Body"].read()

    def delete(self, key: str) -> None:
        self._client.delete_object(Bucket=self._bucket_name, Key=key)


class LocalRepository(AbstractRepository):
    """For testing without consumption of S3 resources"""

    def __init__(self):
        self._upload_folder = Path("uploads")
        self._upload_folder.mkdir(parents=True, exist_ok=True)

    def add(self, data: bytes, key: str) -> None:
        local_path = self._upload_folder / key
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(data)

    def get(self, key: str) -> bytes:
        local_path = self._upload_folder / key
        return local_path.read_bytes()

    def delete(self, key: str) -> None:
        local_path = self._upload_folder / key
        local_path.unlink(missing_ok=True)


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._docs: Dict[str, bytes] = {}

    def add(self, data: bytes, key: str) -> None:
        self._docs[key] = data

    def get(self, key: str) -> bytes:
        return self._docs[key]

    def delete(self, key: str) -> None:
        self._docs.pop(key)
