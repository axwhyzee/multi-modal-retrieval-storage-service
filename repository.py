import logging
from collections import abc
from typing import Dict, Iterator

import boto3  # type: ignore

from config import (
    get_aws_connection_params,
    get_aws_s3_bucket_name,
    get_local_repo_upload_folder,
)

logger = logging.getLogger(__name__)


class AbstractRepository(abc.MutableMapping):
    def __setitem__(self, key: str, value: bytes) -> None:
        raise NotImplementedError

    def __getitem__(self, key: str) -> bytes:
        raise NotImplementedError

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError


class S3Repository(AbstractRepository):
    def __init__(self):
        self._bucket_name = get_aws_s3_bucket_name()
        self._client = boto3.client("s3", **get_aws_connection_params())

    def __setitem__(self, key: str, value: bytes) -> None:
        self._client.put_object(Bucket=self._bucket_name, Key=key, Body=value)

    def __getitem__(self, key: str) -> bytes:
        response = self._client.get_object(Bucket=self._bucket_name, Key=key)
        return response["Body"].read()

    def __delitem__(self, key: str) -> None:
        self._client.delete_object(Bucket=self._bucket_name, Key=key)

    def __iter__(self) -> Iterator[str]:
        for key in self._client.list_objects_v2(Bucket=self._bucket_name):
            yield key

    def __len__(self) -> int:
        return len(list(self.__iter__()))


class LocalRepository(AbstractRepository):
    """For testing without consumption of S3 resources"""

    def __init__(self):
        self._upload_folder = get_local_repo_upload_folder()
        self._upload_folder.mkdir(parents=True, exist_ok=True)

    def __setitem__(self, key: str, value: bytes) -> None:
        local_path = self._upload_folder / key
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(value)

    def __getitem__(self, key: str) -> bytes:
        local_path = self._upload_folder / key
        return local_path.read_bytes()

    def __delitem__(self, key: str) -> None:
        local_path = self._upload_folder / key
        local_path.unlink(missing_ok=True)

    def __iter__(self) -> Iterator[str]:
        for path in self._upload_folder.rglob():
            yield str(path)

    def __len__(self) -> int:
        return len(list(self.__iter__()))


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._docs: Dict[str, bytes] = {}

    def __setitem__(self, key: str, value: bytes) -> None:
        self._docs[key] = value

    def __getitem__(self, key: str) -> bytes:
        return self._docs[key]

    def __delitem__(self, key: str) -> None:
        self._docs.pop(key)

    def __iter__(self) -> Iterator[str]:
        yield from self._docs.keys()

    def __len__(self) -> int:
        return len(self._docs)
