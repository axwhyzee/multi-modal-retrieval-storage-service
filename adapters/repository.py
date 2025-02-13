from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

import boto3

from config import get_aws_bucket_name
from domain.model import DocID


@dataclass
class DocPayload:
    content_type: str
    data: Any


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, doc_id: DocID, doc_payload: DocPayload) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, doc_id: DocID) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, doc_id: DocID) -> DocPayload:
        raise NotImplementedError


class S3Repository:
    def __init__(self):
        self._bucket_name = get_aws_bucket_name()
        self._client = boto3.client("s3")

    def add(self, doc_id: DocID, doc_payload: DocPayload) -> None:
        if doc_payload.content_type == "binary/octet-stream":
            self._client.put_object(
                Bucket=self._bucket_name, Key=doc_id, Body=doc_payload.data
            )
        else:
            raise ValueError(f"Unrecognized content-type {doc_payload.content_type}")

    def delete(self, doc_id: DocID) -> None:
        self._client.delete_object(Bucket=self._bucket_name, Key=doc_id)

    def get(self, doc_id: DocID) -> DocPayload:
        response = self._client.get_object(Bucket=self._bucket_name, Key=doc_id)
        data = response["Body"].read()
        content_type = response["ContentType"]
        return DocPayload(data=data, content_type=content_type)
