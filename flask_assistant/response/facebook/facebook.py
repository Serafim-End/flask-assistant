
from typing import Optional, List, Any

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
from flask_assistant import FACEBOOK


class Facebook(TypesInterface, ListInterface,
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

        self.items = []

        self._message_template = {
            'platform': FACEBOOK,
        }

    def card(self, title: str, subtitle: Optional[str] = None,
             img_url: Optional[str] = None, buttons: Optional[Any] = None,
             **kwargs) -> 'TypesInterface':
        pass

    def quick_replies(self, replies: List[str], title: Optional[str] = None,
                      **kwargs) -> 'TypesInterface':
        pass

    def link_out(self, name: str, url: str, **kwargs) -> 'TypesInterface':
        pass

    def add_item(self, title: str, key: Optional[str] = None,
                 synonyms: Optional[List[str]] = None,
                 description: Optional[str] = None,
                 image: Optional[Any] = None) -> None:
        pass

    def list(self, **kwargs) -> None:
        pass

    def carousel(self, **kwargs) -> None:
        pass

    def permission(self, permissions: List[str], context: Optional[str] = None,
                   update_intent: Optional[str] = None) -> None:
        pass

    def event(self, event: str, **kwargs) -> None:
        pass
