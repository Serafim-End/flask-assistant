
from ... import e


class Button:

    def __init__(self, title: str, **kwargs):

        self.title = e(title)
        self.callback_data = kwargs.get('callback_data')
        self.url = kwargs.get('url')
        self.request_location = kwargs.get('request_location')

    def to_dict(self) -> dict:
        d = {
            'text': self.title,
        }

        if self.callback_data:
            d['callback_data'] = self.callback_data

        elif self.url:
            d['url'] = self.url

        if self.request_location:
            d['request_location'] = self.request_location

        return d
