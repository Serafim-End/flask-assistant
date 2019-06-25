
from typing import Optional, List, Any, Dict
from itertools import zip_longest
from copy import deepcopy

from jinja2 import Template

from flask_assistant.response.dialogflow.types import Text

from flask_assistant.response.base import (
    TypesInterface,
    PermissionInterface, EventInterface, ListInterface
)
from flask_assistant.response.response import _Response

from .types import Button
from .. import e


class Telegram(TypesInterface, ListInterface,
               PermissionInterface, EventInterface):

    HORIZONTAL_KEYBOARD_SPLIT = 2
    SHARE_LOCATION = 'Поделиться своей геопозицией'
    SELECT_TEXT = 'Пожалуйста нажмите на кнопку ниже, чтобы выбрать опцию'
    KEYBOARD_MODE = 'inline_keyboard'

    def __init__(self, response_obj: _Response, **kwargs):
        """
        :param response_obj:
        :param kwargs:
        display_text, is_ssml
        """
        self.response_obj = response_obj

        self.items = []

        # used for DialogFlow base entities
        self._message_template = {
            'platform': 'TELEGRAM'
        }

        # base message for integration
        self.ff_base_payload = {
            'platform': 'TELEGRAM',
            'payload': {
                'telegram': {}
            }
        }

        # message that gonna be composed
        self.ff_payload = deepcopy(self.ff_base_payload)

        if self.response_obj.speech:
            self.__default_text()
        self.response_obj.messages.append(self.ff_payload)

    def __default_text(self):
        msg = deepcopy(self._message_template)
        msg.update(Text([self.response_obj.speech]).to_dict())
        self.response_obj.messages.append(msg)

    def __keyboard_replies(self, replies: List[str],
                           title: Optional[str] = None,
                           **kwargs) -> TypesInterface:
        _l = self.ff_payload['payload']['telegram']
        _l['text'] = (title if title else self.SELECT_TEXT)

        chunks_replies = list(
            zip_longest(
                *[iter(replies)] * self.HORIZONTAL_KEYBOARD_SPLIT,
                fillvalue=None
            )
        )

        _l['reply_markup'] = {
            'one_time_keyboard': True,
            'resize_keyboard': True,
            'keyboard': [
                [
                    {
                        'text': v,
                        'callback_data': v
                    } for v in chunk if v
                ] for chunk in chunks_replies
            ]
        }

        return self

    def __keyboard(self, msg: Dict, buttons: List[Button]):
        chunks = list(
            zip_longest(
                *[iter(buttons)] * self.HORIZONTAL_KEYBOARD_SPLIT,
                fillvalue=None
            )
        )

        d = [[v.to_dict() for v in chunk if v] for chunk in chunks]

        if 'reply_markup' in msg:
            for e in d:
                msg['reply_markup'][self.KEYBOARD_MODE].append(e)
        else:
            msg['reply_markup'] = {self.KEYBOARD_MODE: d}

        return msg

    def tell(self, **kwargs):
        return self

    def ask(self, **kwargs):
        return self

    def card(self, title: str, subtitle: Optional[str] = None,
             img_url: Optional[str] = None, buttons: Optional[Any] = None,
             **kwargs) -> 'TypesInterface':

        t = Template(
            ""
            "*{{title}}*"
            "{{subtitle}}"
            "[{{title}}]({{img_url}})"
            ""
        )

        _l = self.ff_payload['payload']['telegram']
        _l['text'] = t.render(title=title, subtitle=title, img_url=img_url)
        _l['parse_mode'] = 'Markdown'

        if buttons:

            tg_b = [
                Button(
                    title=b.text,
                    callback_data=b.key,
                    url=b.url,
                    **b
                ) for b in buttons
            ]

            _l = self.__keyboard(_l, tg_b)

        return self

    def quick_replies(self, replies: List[str], title: Optional[str] = None,
                      **kwargs) -> 'TypesInterface':

        _l = self.ff_payload['payload']['telegram']
        _l['text'] = (title if title else self.SELECT_TEXT)

        replies_buttons = [
            Button(title=r, callback_data=r) for r in replies
        ]

        _l = self.__keyboard(_l, replies_buttons)
        return self

    def ask_location(self, title: str,
                     button_title: Optional[str] = None) -> 'TypesInterface':

        _l = self.ff_payload['payload']['telegram']

        _l['text'] = title if title else '',
        _l['reply_markup'] = {
          'one_time_keyboard': True,
          'resize_keyboard': True,
          'keyboard': [
            [
              {
                'text': (self.SHARE_LOCATION if not button_title
                         else button_title),
                'callback_data': 'location',
                'request_location': True
              }
            ]
          ]
        }

        return self

    def link_out(self, name: str, url: str, **kwargs) -> 'TypesInterface':
        """
        :param name:
        :param url:
        :param kwargs:
        :return:
        """
        _l = self.ff_payload['payload']['telegram']
        _l['text'] = self.SELECT_TEXT

        tg_b = [Button(title=name, url=url)]
        _l = self.__keyboard(_l, tg_b)
        return self

    def add_item(self, title: str, key: Optional[str] = None,
                 synonyms: Optional[List[str]] = None,
                 description: Optional[str] = None,
                 image: Optional[Any] = None, **kwargs) -> None:

        t = Template(
            ""
            "*{{title}}* \n"
            "{{subtitle}} \n"
            "[{{title}}]({{img_url}})"
            ""
        )

        temp = deepcopy(self.ff_base_payload)
        _l = temp['payload']['telegram']
        _l['text'] = t.render(
            title=e(title),
            subtitle=e(description),
            img_url=image.img_url

        )
        _l['parse_mode'] = 'Markdown'

        tg_b = []

        buttons = kwargs.get('buttons')
        if buttons:
            for b in buttons:
                tg_b.append(
                    Button(
                        title=b.text,
                        callback_data=b.key,
                        url=b.url,
                        **b
                    )
                )

        url = kwargs.get('url')
        if url:
            tg_b.append(Button(title=title, url=url))

        _l = self.__keyboard(_l, tg_b)

        self.items.append(temp)

    def list(self, **kwargs) -> None:
        for e in self.items:
            self.response_obj.messages.append(e)

    def carousel(self, **kwargs) -> None:
        return self.list(**kwargs)

    def permission(self, permissions: List[str], context: Optional[str] = None,
                   update_intent: Optional[str] = None) -> None:
        pass

    def event(self, event: str, **kwargs) -> None:
        pass
