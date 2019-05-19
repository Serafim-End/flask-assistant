
from .base import BaseSerializer


class Payload(BaseSerializer):
    """
    for custom payloads
    """

    def __init__(self, payload: str):
        self.payload = payload

    def to_dict(self) -> dict:
        d = {
            'payload': self.payload
        }

        return d
