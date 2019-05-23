
from typing import Optional, List, Any

from .. import e

from flask import json

from flask_assistant.response.dialogflow.types import (
    Image, QuickReplies, Text, Card
)

from flask_assistant.response.dialogflow.types import Button as ButtonDF
from flask_assistant.response.facebook.types import Button
from flask_assistant.response.base import (
    TypesInterface,
    PermissionInterface, EventInterface, ListInterface
)
from flask_assistant.response.response import _Response


class Facebook(TypesInterface, ListInterface,
               PermissionInterface, EventInterface):

    def __init__(self, response_obj: _Response,
                 display_text: Optional[str] = None,
                 **kwargs):
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

        # used for our templates, but it supports
        # types: media, audio, file, text
        self._payload_template = {
            'attachment': {
                'type': 'template',
                'payload': {}
            }
        }

        self.ff_payload = {
            'payload': {
                'facebook': {}
            }
        }

        self.__default_text()

    def __custom_payload(self, msg: Any):
        _msg = self._message_template.copy()
        _msg['payload'] = {
            'facebook': msg
        }

        self.response_obj.messages.append(_msg)

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

        msg = self._message_template.copy()
        msg.update(Card(title, subtitle, img_url, buttons).to_dict())
        self.response_obj.messages.append(msg)
        return self

    def quick_replies(self, replies: List[str], title: Optional[str] = None,
                      **kwargs) -> 'TypesInterface':
        msg = self._message_template.copy()
        msg.update(QuickReplies(replies, title).to_dict())
        self.response_obj.messages.append(msg)
        return self

    def link_out(self, name: str, url: str, **kwargs) -> 'TypesInterface':
        pass

    def add_item(self, title: str, key: Optional[str] = None,
                 synonyms: Optional[List[str]] = None,
                 description: Optional[str] = None,
                 image: Optional[Image] = None,
                 buttons: Optional[List[Button]] = None,
                 **kwargs) -> None:

        d = {
            'title': e(title),
            'subtitle': e(description),
            'image_url': image.img_url,

            'buttons': [
                {
                    'type': 'postback',
                    'title': title,
                    'payload': key
                }
            ]
        }

        url = kwargs.get('url')
        if url:
            d['default_action'] = {
                'type': 'web_url',
                'url': url,
                'webview_height_ratio': 'tall',
            }

        if buttons:
            for b in buttons:
                d['buttons'].append(b.to_dict())

        self.items.append(d)

    def list(self, buttons: Optional[List[Button]] = None, **kwargs) -> None:
        msg = self._payload_template.copy()
        msg['attachment']['payload'] = {
            'template_type': 'list',
            'top_element_style': 'compact',
            'elements': self.items
        }

        if buttons:
            msg['attachment']['payload']['buttons'] = [
                b.to_dict for b in buttons
            ]

        self.__custom_payload(msg)

    def carousel(self, **kwargs) -> None:
        pass

    def permission(self, permissions: List[str], context: Optional[str] = None,
                   update_intent: Optional[str] = None) -> None:
        pass

    def event(self, event: str, **kwargs) -> None:
        pass
