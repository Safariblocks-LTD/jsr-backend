import string
import random
from .constants import Constant
from django.conf import settings

    
class Generator:
    
    @staticmethod
    def generate_numbers(length=6):
        return "".join(random.choice(string.digits) for _ in range(length))
    
    @classmethod
    def generate_mobile_otp(cls):
        return cls.generate_numbers() if settings.TWILIO_SWITCH else Constant.TWILIO_DEFAULT_OTP