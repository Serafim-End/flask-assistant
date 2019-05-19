
from typing import Optional, List

from ... import e

from .base import BaseSerializer


class QuickReplies(BaseSerializer):

    def __init__(self, quick_replies: List[str],
                 title: Optional[str] = None):

        self.title = e(title)
        self.quick_replies = quick_replies

    def to_dict(self) -> dict:

        d = {
            'quickReplies': self.quick_replies
        }

        if self.title:
            d['title'] = self.title

        return d
