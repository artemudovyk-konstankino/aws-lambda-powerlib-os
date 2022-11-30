from __future__ import annotations

import json
from dataclasses import dataclass

from .event import Event


@dataclass
class ApiGatewayRestEvent(Event):
    """Event class for API Gateway events."""

    resource: str
    path: str
    httpMethod: str
    request_context: dict
    headers: dict
    multi_value_headers: dict
    query_string_parameters: dict
    multi_value_string_parameters: dict
    path_parameters: dict
    stage_variables: dict
    body: dict
    is_base_64_encoded: bool

    def __post_init__(self):
        if not self.query_string_parameters:
            self.query_string_parameters = {}

        if not self.multi_value_string_parameters:
            self.multi_value_string_parameters = {}

        if not self.path_parameters:
            self.path_parameters = {}

        if not self.stage_variables:
            self.stage_variables = {}

    @classmethod
    def from_lambda_event(cls, event: dict) -> ApiGatewayRestEvent:
        if event.get('body'):
            try:
                event['body'] = json.loads(event['body'])
            except json.JSONDecodeError:
                pass

        return cls(
            raw_event=event,
            resource=event.get('resource'),
            path=event.get('path'),
            httpMethod=event.get('httpMethod'),
            request_context=event.get('requestContext', {}),
            headers=event.get('headers', {}),
            multi_value_headers=event.get('multiValueHeaders', {}),
            query_string_parameters=event.get('queryStringParameters', {}),
            multi_value_string_parameters=event.get(
                'multiValueQueryStringParameters', {}
            ),
            path_parameters=event.get('pathParameters', {}),
            stage_variables=event.get('stageVariables', {}),
            body=event.get('body'),
            is_base_64_encoded=event.get('isBase64Encoded'),
        )
