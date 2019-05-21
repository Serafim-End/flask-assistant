
from ... import e


class Button:

    def __init__(self, text: str, url: str):
        self.text = e(text)
        self.url = url

    def to_dict(self) -> dict:
        d = {
            'title': self.text,
            'openUriAction': {
                'uri': self.url
            }
        }

        return d
