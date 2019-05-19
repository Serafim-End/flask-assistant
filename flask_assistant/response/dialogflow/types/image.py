
from typing import Optional

from emoji import emojize as _

from .base import BaseSerializer


class Image(BaseSerializer):

    def __init__(self, img_url: str,
                 accessibility_text: Optional[str] = None):

        self.img_url = img_url
        self.accessibility_text = accessibility_text

    def to_dict(self) -> dict:

        d = {
            'imageUri': self.img_url
        }

        if self.accessibility_text:
            d['accessibilityText'] = e(self.accessibility_text),

        return d
