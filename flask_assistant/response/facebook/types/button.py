
from ... import e


class Button:

    def __init__(self, type: str, title: str, **kwargs):

        self.type = type
        self.title = e(title)
        self.payload = kwargs.get('payload')

        self.url = kwargs.get('url')

    def to_dict(self) -> dict:
        d = {
            'title': self.title,
            'type': self.type
        }

        if self.payload:
            d['payload'] = self.payload

        elif self.url:
            d['url'] = self.url

        return d
