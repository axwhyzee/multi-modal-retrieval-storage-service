from abc import ABC, abstractmethod

import boto3

from config import get_aws_connection_params, get_aws_s3_bucket_name


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, doc_id: str, doc_bytes: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, doc_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, doc_id: str) -> bytes:
        raise NotImplementedError


class S3Repository(AbstractRepository):
    def __init__(self):
        self._bucket_name = get_aws_s3_bucket_name()
        self._client = boto3.client("s3", **get_aws_connection_params())

    def add(self, doc_id: str, doc_bytes: bytes) -> None:
        self._client.put_object(Bucket=self._bucket_name, Key=doc_id, Body=doc_bytes)

    def delete(self, doc_id: str) -> None:
        self._client.delete_object(Bucket=self._bucket_name, Key=doc_id)

    def get(self, doc_id: str) -> bytes:
        response = self._client.get_object(Bucket=self._bucket_name, Key=doc_id)
        return response["Body"].read()
