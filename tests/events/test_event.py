from aws_lambda_powerlib.events.event import Event


def test_init():
    event = Event(raw_event={})
    assert event.raw_event == {}
