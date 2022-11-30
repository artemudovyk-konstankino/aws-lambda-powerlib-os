import pytest

from aws_lambda_powerlib.events import SqsEvent, SqsEventAttributes


@pytest.fixture
def sqs_event() -> dict:
    return {
        'Records': [
            {
                'messageId': '059f36b4-87a3-44ab-83d2-661975830a7d',
                'receiptHandle': 'AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...',
                'body': 'Test message.',
                'attributes': {
                    'ApproximateReceiveCount': '1',
                    'SentTimestamp': '1545082649183',
                    'SenderId': 'AIDAIENQZJOLO23YVJ4VO',
                    'ApproximateFirstReceiveTimestamp': '1545082649185',
                },
                'messageAttributes': {},
                'md5OfBody': 'e4e68fb7bd0e697a0ae8f1bb342846b3',
                'eventSource': 'aws:sqs',
                'eventSourceARN': 'arn:aws:sqs:us-east-2:123456789012:my-queue',
                'awsRegion': 'us-east-2',
            },
        ]
    }


@pytest.fixture
def sqs_event_multiple_record() -> dict:
    return {
        'Records': [
            {
                'messageId': '059f36b4-87a3-44ab-83d2-661975830a7d',
                'receiptHandle': 'AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...',
                'body': 'Test message.',
                'attributes': {
                    'ApproximateReceiveCount': '1',
                    'SentTimestamp': '1545082649183',
                    'SenderId': 'AIDAIENQZJOLO23YVJ4VO',
                    'ApproximateFirstReceiveTimestamp': '1545082649185',
                },
                'messageAttributes': {},
                'md5OfBody': 'e4e68fb7bd0e697a0ae8f1bb342846b3',
                'eventSource': 'aws:sqs',
                'eventSourceARN': 'arn:aws:sqs:us-east-2:123456789012:my-queue',
                'awsRegion': 'us-east-2',
            },
            {
                'messageId': '2e1424d4-f796-459a-8184-9c92662be6da',
                'receiptHandle': 'AQEBzWwaftRI0KuVm4tP+/7q1rGgNqicHq...',
                'body': 'Test message.',
                'attributes': {
                    'ApproximateReceiveCount': '1',
                    'SentTimestamp': '1545082650636',
                    'SenderId': 'AIDAIENQZJOLO23YVJ4VO',
                    'ApproximateFirstReceiveTimestamp': '1545082650649',
                },
                'messageAttributes': {},
                'md5OfBody': 'e4e68fb7bd0e697a0ae8f1bb342846b3',
                'eventSource': 'aws:sqs',
                'eventSourceARN': 'arn:aws:sqs:us-east-2:123456789012:my-queue',
                'awsRegion': 'us-east-2',
            },
        ]
    }


@pytest.fixture
def sqs_fifo_event() -> dict:
    return {
        'Records': [
            {
                'messageId': '11d6ee51-4cc7-4302-9e22-7cd8afdaadf5',
                'receiptHandle': 'AQEBBX8nesZEXmkhsmZeyIE8iQAMig7qw...',
                'body': 'Test body',
                'attributes': {
                    'ApproximateReceiveCount': '1',
                    'SentTimestamp': '1573251510774',
                    'SequenceNumber': '18849496460467696128',
                    'MessageGroupId': '1',
                    'SenderId': 'AIDAIO23YVJENQZJOL4VO',
                    'MessageDeduplicationId': '1',
                    'ApproximateFirstReceiveTimestamp': '1573251510774',
                },
                'messageAttributes': {},
                'md5OfBody': 'e4e68fb7bd0e697a0ae8f1bb342846b3',
                'eventSource': 'aws:sqs',
                'eventSourceARN': 'arn:aws:sqs:us-east-2:123456789012:fifo.fifo',
                'awsRegion': 'us-east-2',
            },
            {
                'messageId': '2e1424d4-f796-459a-8184-9c92662be6da',
                'receiptHandle': 'AQEBzWwaftRI0KuVm4tP+/7q1rGgNqicHq...',
                'body': 'Test message.',
                'attributes': {
                    'ApproximateReceiveCount': '1',
                    'SentTimestamp': '1545082650636',
                    'SequenceNumber': '18849496460467696128',
                    'MessageGroupId': '1',
                    'SenderId': 'AIDAIO23YVJENQZJOL4VO',
                    'MessageDeduplicationId': '1',
                    'ApproximateFirstReceiveTimestamp': '1545082650636',
                },
                'messageAttributes': {},
                'md5OfBody': 'e4e68fb7bd0e697a0ae8f1bb342846b3',
                'eventSource': 'aws:sqs',
                'eventSourceARN': 'arn:aws:sqs:us-east-2:123456789012:my-queue',
                'awsRegion': 'us-east-2',
            },
        ]
    }


def test_init(sqs_event: dict) -> None:
    """SqsEvent object properties should be initialized correctly from lambda event."""
    event = SqsEvent.from_lambda_event(sqs_event)[0]
    assert event.body == sqs_event['Records'][0]['body']
    assert event.message_id == sqs_event['Records'][0]['messageId']
    assert event.receipt_handle == sqs_event['Records'][0]['receiptHandle']
    assert event.attributes == SqsEventAttributes.from_dict(
        sqs_event['Records'][0]['attributes']
    )
    assert event.message_attributes == sqs_event['Records'][0]['messageAttributes']
    assert event.md5_of_body == sqs_event['Records'][0]['md5OfBody']
    assert event.event_source == sqs_event['Records'][0]['eventSource']
    assert event.event_source_arn == sqs_event['Records'][0]['eventSourceARN']
    assert event.aws_region == sqs_event['Records'][0]['awsRegion']

    # Also the event should be of type 'Standard'
    assert event.type == SqsEvent.Type.STANDARD


def test_multiple_records_init(sqs_event_multiple_record: dict) -> None:
    """Should return multiple events objects if there are multiple records."""
    events = SqsEvent.from_lambda_event(sqs_event_multiple_record)
    assert len(events) == len(sqs_event_multiple_record['Records'])


def test_fifo_init(sqs_fifo_event: dict) -> None:
    """FIFO SQS Event type should have distinct type property
    and intialized related to it fields."""
    event = SqsEvent.from_lambda_event(sqs_fifo_event)[0]
    assert event.type == SqsEvent.Type.FIFO
    assert event.attributes.sequence_number is not None
    assert event.attributes.message_group_id is not None
    assert event.attributes.message_deduplication_id is not None
