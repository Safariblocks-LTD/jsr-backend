import firebase_admin
from firebase_admin import (
    credentials, 
    messaging,
)
from django.conf import settings
from .responder import Responder
from .constants import Constant


class FCM:

    credentials = credentials.Certificate(settings.FIREBASE_KEY)
    firebase_admin.initialize_app(credentials)
    
    @staticmethod
    def validate(fcm_token):
        try:
            message = messaging.Message(token=fcm_token)
            return messaging.send(message)
        except Exception:
            Responder.raise_error(113)
        
    @classmethod
    def send(cls, fcm_token, description, data):
        message = messaging.Message(
            token = fcm_token,
            **cls.__get_args(description, data)
        )
        return messaging.send(message)
        
    @classmethod
    def bulk_send(cls, fcm_tokens, description, data):
        if not fcm_tokens: return
        message = messaging.MulticastMessage(
            tokens = fcm_tokens,
            **cls.__get_args(description, data)
        )
        return messaging.send_multicast(message)
        
    @classmethod
    def __get_args(cls, description, data):
        return {
            "notification": messaging.Notification(
                title = Constant.push_notifications[100],
                body = description
            ),
            "data": {
                key:str(value) for key, value in data.items()
            },
        }