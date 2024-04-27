from .constants import Constant
from rest_framework.response import Response
from jasiri_wallet.exceptions import ApiException


class Responder:
    
    @staticmethod
    def send(code, data=None, status=True, args=None):
        return Response(
            {
                "status": status,
                "code": code,
                "message": eval(Constant.response_messages[code]) if args else Constant.response_messages[code],
                "data": {} if data is None else data,
            },
            status = 200 if status else 400 
        )
        
    @staticmethod
    def raise_error(code, **args):
        raise ApiException(code, args)