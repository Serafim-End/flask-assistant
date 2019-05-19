
from typing import Optional

from ... import e

from .base import BaseSerializer
from .button import Button


class Card(BaseSerializer):

    def __init__(self, title: str, subtitle: str,
                 img_url: Optional[str] = None,
                 buttons: Optional[Button] = None):

        self.title = e(title)
        self.subtitle = e(subtitle)
        self.img_url = img_url
        self.buttons = buttons

    def to_dict(self) -> dict:
        d = {
            'title': self.title,
            'subtitle': self.subtitle,
        }

        if self.img_url:
            d['imageUri'] = self.img_url

        if self.buttons:
            d['buttons'] = self.buttons.to_dict()

        return d
