
from typing import Optional

from flask import json, make_response
from emoji import emojize as _

from flask_assistant import core

from .. import logger


class _Response(object):
    """Base webhook response to be returned to Dialogflow"""

    def __init__(self, speech: Optional[str] = None):

        self.speech = _(speech, use_aliases=True) if speech else speech

        self.messages = [
            {
                'text': {
                    'text': [speech]
                }
            }
        ]

        self.response = {
            'fulfillmentText': speech,
            'fulfillmentMessages': self.messages,
            'payload': {},
            'outputContexts': [],
            'source': 'webhook',

            # TODO event processing support
            "followupEventInput": None
        }

    def _include_contexts(self) -> None:
        for context in core.context_manager.active:
            self.response['outputContexts'].append(context.serialize)

    def render_response(self) -> None:
        self._include_contexts()

        logger.debug(
            json.dumps(self.response, indent=2)
        )

        resp = make_response(json.dumps(self.response))
        resp.headers['Content-Type'] = 'application/json'

        return resp
