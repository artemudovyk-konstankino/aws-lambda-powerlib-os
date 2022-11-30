import json
from dataclasses import dataclass, field
from typing import Union


@dataclass
class ApiResponser:
    """Responser for Lambda functions."""

    status_code: int
    body: Union[dict, str]
    headers: dict = field(
        default_factory=lambda: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
        }
    )

    @property
    def _jsoned_body(self) -> str:
        """Convert body to JSON string."""
        if isinstance(self.body, dict):
            return json.dumps(self.body, default=str)
        else:
            return self.body

    def json(self) -> dict:
        """Convert to Lambda response."""
        return {
            'statusCode': self.status_code,
            'body': self._jsoned_body,
            'headers': self.headers,
        }
