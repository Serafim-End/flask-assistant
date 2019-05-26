
from typing import Optional

from ... import e

from .base import BaseSerializer


class Button(BaseSerializer):

    def __init__(self, text: str,
                 key: Optional[str] = None,
                 **kwargs):

        self.text = e(text)
        self.key = key
        self.url = kwargs.get('url')
        self.kwargs = kwargs

    def to_dict(self) -> dict:
        d = {
            'text': self.text,
            'postback': self.key,
        }

        return d
