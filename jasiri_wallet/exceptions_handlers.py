from django.conf import settings
from jasiri_wallet.exceptions import ApiException
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import (
    MethodNotAllowed, 
    ParseError,
    UnsupportedMediaType,
    NotAcceptable,
    NotFound,
    NotAuthenticated, 
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
)
from utils import (
    Responder, 
    Constant,
    Logger,
)
import traceback
from rest_framework.decorators import api_view
# algosdk.error.AlgodHTTPErro
from algosdk.error import AlgodHTTPError


def errors_handler(exception, context):
    args = None
    if isinstance(exception, ApiException):
        code = exception.error_code
        args = exception.data
    elif isinstance(exception, MethodNotAllowed):
        code = 504
    elif isinstance(exception, ParseError):
        code = 502
    elif isinstance(exception, PermissionDenied):
        code = 509
    elif isinstance(exception, UnsupportedMediaType):
        code = 503
    elif isinstance(exception, (NotAuthenticated, AuthenticationFailed)):
        code = 509
        
    elif isinstance(exception, (ValidationError, DjangoValidationError)):
        code = exception.get_codes()
        if(isinstance(code, dict)):
            code = list(code.values())[0][0]
        if(isinstance(code, list)):
            code = code[0]
        if isinstance(code, str):
            code = Constant.django_default_codes.get(code, 505)
    else:
        code = 500
        Logger.log(context.get("request"), traceback.format_exc())
        if settings.DEBUG:
            raise exception
    return Responder.send(code, args=args, status=False)


@api_view(("GET",))
def hanlder404(request, exception):
    return Responder.send(501, status=False)