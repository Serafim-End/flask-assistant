
from ... import e


class Button:

    def __init__(self, type: str, title: str, **kwargs):

        self.type = type
        self.title = e(title)
        self.payload = kwargs.get('payload')

        # TODO: more variants of button
        # self.url = kwargs.get('')

    def to_dict(self) -> dict:
        d = {
            'title': self.title,
            'payload': self.payload,
            'type': self.type
        }

        return d
