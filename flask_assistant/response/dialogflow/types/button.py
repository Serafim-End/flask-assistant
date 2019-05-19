
from typing import Optional

from ... import e

from .base import BaseSerializer


class Button(BaseSerializer):

    def __init__(self, text: str, url: Optional[str]):
        self.text = e(text)
        self.url = url

    def to_dict(self) -> dict:
        d = {
            'text': self.text
        }

        if self.url:
            d['postback'] = self.url

        return d
