from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .event import Event


@dataclass
class SqsEventAttributes:
    approximate_recieve_count: int
    sent_timestamp: int
    sender_id: str
    approximate_first_recieve_timestamp: int
    sequence_number: Optional[int]
    message_group_id: Optional[int]
    message_deduplication_id: Optional[int]

    @classmethod
    def from_dict(cls, attributes: dict) -> SqsEventAttributes:
        sequence_number = (
            int(attributes.get('SequenceNumber'))
            if attributes.get('SequenceNumber')
            else None
        )
        message_group_id = (
            int(attributes.get('MessageGroupId'))
            if attributes.get('MessageGroupId')
            else None
        )
        message_deduplication_id = (
            int(attributes.get('MessageDeduplicationId'))
            if attributes.get('MessageDeduplicationId')
            else None
        )

        return cls(
            approximate_recieve_count=int(attributes.get('ApproximateReceiveCount')),
            sent_timestamp=int(attributes.get('SentTimestamp')),
            sender_id=attributes.get('SenderId'),
            approximate_first_recieve_timestamp=int(
                attributes.get('ApproximateFirstReceiveTimestamp')
            ),
            sequence_number=sequence_number,
            message_group_id=message_group_id,
            message_deduplication_id=message_deduplication_id,
        )


@dataclass
class SqsEvent(Event):
    """Event class for SQS events."""

    body: str
    message_id: str
    receipt_handle: str
    attributes: SqsEventAttributes
    message_attributes: dict
    md5_of_body: str
    event_source: str
    event_source_arn: str
    aws_region: str

    class Type(Enum):
        STANDARD = 'standard'
        FIFO = 'fifo'

    @property
    def type(self) -> str:
        if (
            self.attributes.sequence_number is not None
            and self.attributes.message_group_id is not None
            and self.attributes.message_deduplication_id is not None
        ):
            return self.Type.FIFO

        return self.Type.STANDARD

    @classmethod
    def from_lambda_event(cls, event: dict) -> list[SqsEvent]:
        sqs_events = [
            cls(
                raw_event=record,
                body=record['body'],
                message_id=record['messageId'],
                receipt_handle=record['receiptHandle'],
                attributes=SqsEventAttributes.from_dict(record['attributes']),
                message_attributes=record['messageAttributes'],
                md5_of_body=record['md5OfBody'],
                event_source=record['eventSource'],
                event_source_arn=record['eventSourceARN'],
                aws_region=record['awsRegion'],
            )
            for record in event['Records']
        ]
        return sqs_events
