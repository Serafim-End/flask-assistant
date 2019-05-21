
from typing import Optional, List

from ... import e

from .button import Button
from ...dialogflow.types import Image


class Card:

    def __init__(self, title: str, subtitle: str,
                 text: Optional[str] = None,
                 img_url: Optional[str] = None,
                 accessibility_text: Optional[str] = None,
                 buttons: Optional[List[Button]] = None):

        self.title = e(title)
        self.subtitle = e(subtitle)
        self.img_url = img_url
        self.accessibility_text = accessibility_text
        self.buttons = buttons
        self.text = text

    def to_dict(self) -> dict:
        d = {
            'basicCard': {
                'title': self.title,
                'subtitle': self.subtitle,
                'formattedText': self.text,
                'image': Image(
                    img_url=self.img_url,
                    accessibility_text=self.accessibility_text
                ).to_dict(),
                'buttons': [b.to_dict() for b in self.buttons]
            }
        }

        return d
