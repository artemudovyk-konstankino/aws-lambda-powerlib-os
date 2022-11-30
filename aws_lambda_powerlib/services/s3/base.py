from dataclasses import dataclass


@dataclass
class S3Service:
    s3_client: object
