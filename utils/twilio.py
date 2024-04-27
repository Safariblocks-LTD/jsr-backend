from django.conf import settings
from twilio.rest import Client
from .constants import Constant
from .responder import Responder


class Twilio:
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    
    @classmethod
    def send(cls, to, code, **kwargs):
        if not settings.TWILIO_SWITCH: return
        body = eval(Constant.twilio_messages[code])
        try:
            cls.client.messages.create(
                to=to,
                body=body,
                from_=settings.TWILIO_NUMBER,
            )
        except Exception:
            Responder.raise_error(512)