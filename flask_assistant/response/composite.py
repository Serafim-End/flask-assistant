from typing import Optional, List

from flask import current_app

from .actions_on_google import ActionsOnGoogle
from .response import _Response
from .base import (TypesInterface, ListInterface)
from .dialogflow.types import Image, Button

INTEGRATIONS = {
    'ACTIONS_ON_GOOGLE': ActionsOnGoogle
}


class _BaseResponseComposite:
    def __init__(self, speech: Optional[str], **kwargs):

        self.response_obj = _Response(speech=speech)

        self._integrations = current_app.config.get('INTEGRATIONS', [])

        self.objs_integrations = {}
        for k in self._integrations:
            if k in INTEGRATIONS:
                self.objs_integrations[k] = INTEGRATIONS[k](
                    self.response_obj, **kwargs
                )

    # TODO: implement property for integration


class _ResponseComposite(_BaseResponseComposite, TypesInterface, ListInterface):

    def __init__(self, speech: str, **kwargs):
        super(_ResponseComposite, self).__init__(speech, **kwargs)

    def card(self, title: str, subtitle: Optional[str] = None,
             img_url: Optional[str] = None,
             buttons: Optional[List[Button]] = None) -> '_ResponseComposite':

        self.objs_integrations = {
            k: v.card(title, subtitle, img_url, buttons)
            for k, v in self.objs_integrations.items()
        }

        return self

    def quick_replies(self, replies: List[str],
                      title: Optional[str] = None) -> '_ResponseComposite':
        self.objs_integrations = {
            k: v.quick_replies(replies, title)
            for k, v in self.objs_integrations.items()
        }

        return self

    def link_out(self, name: str, url: str) -> '_ResponseComposite':
        self.objs_integrations = {
            k: v.link_out(name, url)
            for k, v in self.objs_integrations.items()
        }

        return self

    def add_item(self, title: str, key: Optional[str] = None,
                 synonyms: Optional[List[str]] = None,
                 description: Optional[str] = None,
                 image: Optional[Image] = None) -> None:

        for k, v in self.objs_integrations.items():
            v.add_item(
                title, key, synonyms, description, image
            )

    def list(self, **kwargs) -> None:
        for k, v in self.objs_integrations.items():
            v.list(**kwargs)

    def carousel(self, **kwargs) -> None:
        for k, v in self.objs_integrations.items():
            v.carousel(**kwargs)


class ask(_ResponseComposite):
    def __init__(self, speech: str, **kwargs):
        super(ask, self).__init__(speech, **kwargs)
        self.objs_integrations = {
            k: v.ask(**kwargs)
            for k, v in self.objs_integrations.items()
        }


class tell(_ResponseComposite):
    def __init__(self, speech: str, **kwargs):
        super(tell, self).__init__(speech, **kwargs)
        self.objs_integrations = {
            k: v.tell(**kwargs)
            for k, v in self.objs_integrations.items()
        }


class event(_BaseResponseComposite):
    def __init__(self, event_name: str, **kwargs):
        super(event, self).__init__(speech='', **kwargs)

        for o in self.objs_integrations:
            o.event(event_name)


class permission(_BaseResponseComposite):

    def __init__(self, permissions: List[str],
                 context: Optional[str] = None,
                 update_intent: Optional[str] = None):
        super(permission, self).__init__(speech=None)

        for o in self.objs_integrations:
            o.permission(permissions, context, update_intent)
