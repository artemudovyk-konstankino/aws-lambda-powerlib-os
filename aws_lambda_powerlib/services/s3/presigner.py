from dataclasses import dataclass
from datetime import datetime
from typing import Union

from .base import S3Service


@dataclass
class S3Presigner(S3Service):
    s3_client: object
    bucket: str

    def presign_get(
        self, keys: Union[str, list[str]], expires_in: int = 3600
    ) -> Union[str, list[str]]:
        """Presign download URLS for the given keys. Returns a dict with pairs 'key: presigned url'"""
        # If a single key is passed, return a single presigned URL
        print(keys)
        if isinstance(keys, str):
            print('single')
            return self.s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': keys,
                },
                ExpiresIn=expires_in,
            )

        print('multiple')
        # If a list of keys is passed, return a list of presigned URLs
        presigned_urls = []
        for key in keys:
            presigned_urls.append(
                self.s3_client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={
                        'Bucket': self.bucket,
                        'Key': key,
                    },
                    ExpiresIn=expires_in,
                )
            )
        return presigned_urls

    def presign_post(
        self, keys: list[str], prefix: str = '', expires_in: int = 3600
    ) -> list[dict]:
        """Presigns upload URLs for the given keys. Returns a dict, including POST data for each key."""
        presigned_urls = []
        for key in keys:
            s3_key = f'{prefix}{key}'
            presigned_data = self.s3_client.generate_presigned_post(
                Bucket=self.bucket,
                Key=s3_key,
                ExpiresIn=expires_in,
            )
            presigned_urls.append(
                {
                    'name': key,
                    'url': presigned_data.get('url'),
                    'fields': presigned_data.get('fields'),
                    'key': s3_key,
                    'bucket': self.bucket,
                    'expiresIn': expires_in,
                    'presignedTimestamp': f'{datetime.utcnow().isoformat()}Z',
                }
            )
        return presigned_urls

    def presign_put(
        self, keys: list[str], prefix: str = '', expires_in: int = 3600
    ) -> list[dict]:
        """Presign upload URLS for the given keys. Returns a dict with pairs 'key: presigned url'"""
        presigned_urls = []
        for key in keys:
            s3_key = f'{prefix}{key}'
            url = self.s3_client.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': s3_key,
                },
                ExpiresIn=expires_in,
            )

            presigned_urls.append(
                {
                    'name': key,
                    'url': url,
                    'key': s3_key,
                    'bucket': self.bucket,
                    'expiresIn': expires_in,
                    'presignedTimestamp': f'{datetime.utcnow().isoformat()}Z',
                }
            )
        return presigned_urls
