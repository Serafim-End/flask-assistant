
from typing import Optional

from ... import e

from .base import BaseSerializer


class Button(BaseSerializer):

    def __init__(self, text: str,
                 url: Optional[str] = None,
                 key: Optional[str] = None):

        self.text = e(text)
        self.url = url
        self.key = key

    def to_dict(self) -> dict:
        d = {
            'title': self.text,
            'type': 'postback',

        }

        if self.url:
            d['type'] = 'web_url'
            d['url'] = self.url

        elif self.key:
            d['payload'] = self.key

        return d
