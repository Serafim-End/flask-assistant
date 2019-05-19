
from typing import List

from ... import e

from .base import BaseSerializer


class Text(BaseSerializer):

    def __init__(self, text: List[str]):
        self.text = e(text)

    def to_dict(self) -> dict:

        d = {
            'text': self.text
        }

        return d
