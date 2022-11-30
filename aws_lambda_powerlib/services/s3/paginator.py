from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from .base import S3Service


@dataclass
class PaginatorPage:
    contents: list[dict]
    is_truncated: bool
    continuation_token: str
    next_continuation_token: str
    response_metadata: dict
    bucket_name: str
    prefix: str
    max_keys: int
    keys_count: int
    encoding_type: str

    @classmethod
    def from_dict(cls, data: dict) -> PaginatorPage:
        return cls(
            contents=data.get('Contents'),
            is_truncated=data.get('IsTruncated'),
            continuation_token=data.get('ContinuationToken'),
            next_continuation_token=data.get('NextContinuationToken'),
            response_metadata=data.get('ResponseMetadata'),
            bucket_name=data.get('Name'),
            prefix=data.get('Prefix'),
            max_keys=data.get('MaxKeys'),
            keys_count=data.get('KeyCount'),
            encoding_type=data.get('EncodingType'),
        )

    def json(self):
        # Create deep copy of self
        obj_deep_copy = deepcopy(self.__dict__)

        # Encode LastModified datetime.datetime value to string
        for item in obj_deep_copy['contents']:
            item['LastModified'] = str(item['LastModified'])

        # Return json
        return json.dumps(obj_deep_copy)


@dataclass
class S3Paginator(S3Service):
    bucket: str
    prefix: str = ''
    max_items: int = 1000
    page_size: Optional[int] = None

    def get(
        self,
        starting_token: Optional[str] = None,
    ) -> PaginatorPage:
        # Init PageIterator
        paginator = self.s3_client.get_paginator('list_objects_v2')

        pages = iter(
            paginator.paginate(
                Bucket=self.bucket,
                Prefix=self.prefix,
                PaginationConfig={
                    'MaxItems': self.max_items,
                    'StartingToken': starting_token,
                    'PageSize': self.page_size,
                },
            )
        )

        # Get first page and init PaginatorPage object from dict
        page = next(pages)
        print('page', page)

        return PaginatorPage.from_dict(page)
