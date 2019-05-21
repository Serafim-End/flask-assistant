
from typing import Optional, List

from .. import e

from flask import json

from flask_assistant.response.dialogflow.types import Image
from flask_assistant.response.dialogflow.types import Button as ButtonDF
from flask_assistant.response.actions_on_google.types import Card, Button
from flask_assistant.response.base import (
    TypesInterface,
    PermissionInterface, EventInterface, ListInterface
)
from flask_assistant.response.response import _Response
from flask_assistant import ACTIONS_ON_GOOGLE

class ActionsOnGoogle(TypesInterface, ListInterface,
                      PermissionInterface, EventInterface):

    def __init__(self, response_obj: _Response,
                 display_text: Optional[str] = None,
                 is_ssml: Optional[bool] = False, **kwargs):
        """
        :param response_obj:
        :param kwargs:
        display_text, is_ssml
        """
        self.response_obj = response_obj

        self.response_obj.response['payload']['google'] = {
            'expect_user_response': True,
            'is_ssml': True,
            'permissions_request': None,
        }

        self.items = []

        self._message_template = {
            'platform': ACTIONS_ON_GOOGLE,
        }

        self._integrate_with_actions(
            self.response_obj.speech,
            display_text,
            is_ssml
        )

    def _set_user_storage(self) -> None:
        from flask_assistant.core import user

        # If empty or unspecified,
        # the existing persisted token will be unchanged.
        user_storage = user.get('userStorage')
        if not user_storage:
            return

        if isinstance(user_storage, dict):
            user_storage = json.dumps(user_storage)

        if len(user_storage.encode('utf-8')) > 10000:
            raise ValueError('UserStorage must not exceed 10k bytes')

        self.response_obj.response['payload']['google']['userStorage'] = user_storage

    def _integrate_with_actions(self, speech: Optional[str] = None,
                                display_text: Optional[str] = None,
                                is_ssml: Optional[bool] = False) -> None:
        if not display_text:
            display_text = speech

        msg = self._message_template.copy()

        simple_response = {'displayText': display_text}
        if is_ssml:
            ssml_speech = "<speak>" + speech + "</speak>"
            simple_response['ssml'] = ssml_speech
        else:
            simple_response['textToSpeech'] = speech

        d = {
            'simpleResponses': {
                'simpleResponses': [simple_response]
            }
        }

        msg.update(d)
        self.response_obj.messages.append(msg)

    def card(self, title: str,
             subtitle: Optional[str] = None,
             img_url: Optional[str] = None,
             buttons: Optional[List[ButtonDF]] = None,
             **kwargs) -> 'TypesInterface':

        msg = self._message_template.copy()

        if buttons:
            buttons = [Button(b.text, b.url) for b in buttons]

        msg.update(
            Card(
                title=title,
                subtitle=subtitle,
                img_url=img_url,
                buttons=buttons,
                **kwargs
            ).to_dict()
        )
        self.response_obj.messages.append(msg)
        return self

    def quick_replies(self, replies: List[str],
                      title: Optional[str] = None,
                      **kwargs) -> 'TypesInterface':

        msg = self._message_template.copy()

        suggestions = {
            'suggestions': {
                'suggestions': [
                    {'title': e(r)} for r in replies
                ]
            }
        }

        msg.update(suggestions)
        self.response_obj.messages.append(msg)
        return self

    def link_out(self, name: str, url: str, **kwargs) -> 'TypesInterface':
        msg = self._message_template.copy()

        link_out = {
            'linkOutSuggestion': {
                'destinationName': e(name),
                'uri': url
            }
        }

        msg.update(link_out)
        self.response_obj.messages.append(msg)
        return self

    def tell(self, **kwargs):
        self.response_obj.response['payload']['google']['expect_user_response'] = False
        return self

    def ask(self, **kwargs):
        self.response_obj.response['payload']['google']['expect_user_response'] = True
        return self

    def add_item(self, title: str,
                 key: Optional[str] = None,
                 synonyms: Optional[List[str]] = None,
                 description: Optional[str] = None,
                 image: Optional[Image] = None) -> None:

        d = {
            'info': {
                'key': e(key) or e(title),
                'synonyms': synonyms or []
            },

            'title': e(title),
            'description': e(description),
        }

        if image:
            d['image'] = image.to_dict()

        self.items.append(d)

    def list(self, title: Optional[str] = None, **kwargs) -> None:

        if not self.items:
            raise Exception('Add items before list building')

        msg = self._message_template.copy()

        list_select = {
            'listSelect': {
                'title': e(title),
                'items': self.items}
        }

        msg.update(list_select)
        self.response_obj.messages.append(msg)

    def carousel(self, **kwargs) -> None:
        if not self.items:
            raise Exception('Add items before carousel building')

        msg = self._message_template.copy()

        carousel_select = {
            'carouselSelect': {
                'items': self.items
            }
        }

        msg.update(carousel_select)
        self.response_obj.messages.append(msg)

    def event(self, event: str, **kwargs) -> None:
        self.response_obj.speech = ''
        self.response_obj.response['followupEventInput'] = {
            'name': event,
            'parameters': kwargs,
        }

    def permission(self, permissions: List[str],
                   context: Optional[str] = None,
                   update_intent: Optional[str] = None) -> None:

        self.response_obj.speech = None
        self.response_obj.messages[:] = []

        if 'UPDATE' in permissions and not update_intent:
            raise ValueError('update_intent is required '
                             'to ask for UPDATE permission')

        self.response_obj.response['payload']['google']['systemIntent'] = {
            'intent': 'actions.intent.PERMISSION',
            'data': {
                '@type': 'type.googleapis.com/google.actions.v2.PermissionValueSpec',
                'optContext': context,
                'permissions': permissions,
                'updatePermissionValueSpec': {'intent': update_intent},
            },
        }
