
from emoji import emojize

e = lambda o: emojize(o, use_aliases=True)


from .composite import ask, tell, event, permission

from .dialogflow.types import Button, Image

from .composite import _BaseResponseComposite, _ResponseComposite

ACTIONS_ON_GOOGLE = 'ACTIONS_ON_GOOGLE'
FACEBOOK = 'FACEBOOK'

# TELEGRAM = 'TELEGRAM'
# KIK = 'KIK'
# SKYPE = 'SKYPE'
# LINE = 'LINE'
# VIBER = 'VIBER'
# SLACK = 'SLACK'
