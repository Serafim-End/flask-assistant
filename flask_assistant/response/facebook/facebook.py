
from typing import Optional, List, Any

from .. import e

from flask_assistant.response.dialogflow.types import Image, Text

from flask_assistant.response.dialogflow.types import Button as ButtonDF
from flask_assistant.response.facebook.types import Button
from flask_assistant.response.base import (
    TypesInterface,
    PermissionInterface, EventInterface, ListInterface
)
from flask_assistant.response.response import _Response


class Facebook(TypesInterface, ListInterface,
               PermissionInterface, EventInterface):

    def __init__(self, response_obj: _Response, **kwargs):
        """
        :param response_obj:
        :param kwargs:
        display_text, is_ssml
        """
        self.response_obj = response_obj

        self.items = []

        self._message_template = {
            'platform': 'FACEBOOK'
        }

        self.ff_payload = {
            'platform': 'FACEBOOK',
            'payload': {
                'facebook': {}
            }
        }

        if self.response_obj.speech:
            self.__default_text()
        self.response_obj.messages.append(self.ff_payload)

    def __default_text(self):
        msg = self._message_template.copy()
        msg.update(Text([self.response_obj.speech]).to_dict())
        self.response_obj.messages.append(msg)

    def tell(self, **kwargs):
        return self

    def ask(self, **kwargs):
        return self

    def card(self, title: str, subtitle: Optional[str] = None,
             img_url: Optional[str] = None, buttons: Optional[Any] = None,
             **kwargs) -> 'TypesInterface':

        self.ff_payload['payload']['facebook']['attachment'] = {}
        self.add_item(
            title=title,
            key=title,
            synonyms=None,
            description=subtitle,
            image=Image(img_url=img_url),
            buttons=buttons,
            expanded_view=True
        )

        self.carousel()
        return self

    def quick_replies(self, replies: List[str],
                      title: Optional[str] = None,
                      **kwargs) -> 'TypesInterface':

        _l = self.ff_payload['payload']['facebook']

        quick_replies = []

        for e in replies:
            quick_replies.append(
                {
                    'content_type': 'text',
                    'title': e,
                    'payload': e
                }
            )

        _l['quick_replies'] = quick_replies
        return self

    def ask_location(self):

        _l = self.ff_payload['payload']['facebook']

        location = {
            'content_type': 'location'
        }

        if 'quick_replies' in _l:
            _l['quick_replies'].append(location)
        else:
            _l['quick_replies'] = {'quick_replies': [location]}
        return self

    def link_out(self, name: str, url: str, **kwargs) -> 'TypesInterface':
        """
        this method is not implemented by this platform and will be ignored
        :param name:
        :param url:
        :param kwargs:
        :return:
        """
        return self

    def add_item(self, title: str, key: Optional[str] = None,
                 synonyms: Optional[List[str]] = None,
                 description: Optional[str] = None,
                 image: Optional[Image] = None,
                 buttons: Optional[List[ButtonDF]] = None,
                 expanded_view: Optional[bool] = False,
                 **kwargs) -> None:

        d = {
            'title': e(title),
            'subtitle': e(description),
        }

        if image:
            d['image_url'] = image.img_url

        if not expanded_view:
            d['buttons'] = [
                {
                    'type': 'postback',
                    'title': title,
                    'payload': key
                }
            ]

        url = kwargs.get('url')
        if url:
            d['default_action'] = {
                'type': 'web_url',
                'url': url,
                'webview_height_ratio': 'tall',
            }

        if buttons:
            if 'buttons' not in d:
                d['buttons'] = []

            for b in buttons:
                fb_b = Button(
                    type='web_url',
                    title=b.text,
                    url=b.url
                )

                d['buttons'].append(fb_b.to_dict())

        self.items.append(d)

    def list(self, buttons: Optional[List[ButtonDF]] = None, **kwargs):

        self.ff_payload['payload']['facebook']['attachment'] = {}

        _l = {
            'type': 'template',
            'payload': {
                'template_type': 'list',
                'top_element_style': 'compact',
                'elements': self.items
            }
        }

        if buttons:

            _l['payload']['buttons'] = [
                Button(
                    type='web_url',
                    title=b.text,
                    **b.kwargs
                ).to_dict for b in buttons
            ]

        self.ff_payload['payload']['facebook']['attachment'] = _l
        return self

    def carousel(self, **kwargs):

        self.ff_payload['payload']['facebook']['attachment'] = {}

        _l = {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'elements': self.items
            }
        }

        self.ff_payload['payload']['facebook']['attachment'] = _l
        return self

    def permission(self, permissions: List[str], context: Optional[str] = None,
                   update_intent: Optional[str] = None) -> None:
        pass

    def event(self, event: str, **kwargs) -> None:
        pass
