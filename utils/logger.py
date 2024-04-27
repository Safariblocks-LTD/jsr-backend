from django.utils.timezone import localtime
from django.conf import settings
from loguru import logger
from .constants import Constant
from .email import Email
from ipware import get_client_ip
from pytz import timezone
from django.core.cache import cache


class Logger:
    
    log_file = f"{settings.BASE_DIR}/logs/{{time:D-MMM-YYYY}}.log"
    logger.add(log_file, format="{message}", rotation="1 days", level="INFO")
    
    @classmethod
    def log(cls, request, response, execution_time=None):
        if settings.DEBUG: return None
        current_time = localtime(timezone=timezone("Asia/Kolkata")).strftime("%I:%M:%S %p (%Z)")
        headers = {key:value for key, value in request.headers.items() if key in Constant.HEADER_KEYS.split()}
        ip, _ = get_client_ip(request)
        data = f"""
            {current_time} | IP [{ip}]
            {request.build_absolute_uri()} ({request.method})
            HEADERS {headers}\n"""
        data = cls.__get_log_data(execution_time, response, data, request, current_time)
        logger.info(data)
                
    @classmethod
    def __get_log_data(cls, execution_time, response, data, request, current_time):
        if execution_time is None:
            data += f"""STATUS [False] | STATUS_CODE [500 ~ Server Error]
            
            xxxxxxxxxxxxxxxxxxxx [ERROR] xxxxxxxxxxxxxxxxxxxxxxxxxx
            {response}"""
            cls.__notify_devs(data)
        else:
            data += f"""STATUS [{response.data.get('status')}] | STATUS_CODE [{response.data.get('code')} ~ {Constant.response_messages[response.data.get('code')]}] | TIME_TAKEN [{round(execution_time, 3)} Seconds]\n"""
        data += "\n************************************************************************************************************"
        return data.replace("  ","")
    
    
    @staticmethod
    def __notify_devs(error):
        error = f"Something went wrong on the server, please see below for the more details\n{error}".replace("  ", "")
        Email.send_server_error.delay(error)

    @classmethod
    def custom_log(cls, error):
        logger.info(error)

    @classmethod
    def api_call_count(cls):
        key = "api_call_count"
        if not cache.get(key):
            cache.set(key, 1, 7*24*60*60)
        else:
            cache.set(key, cache.get(key) + 1, 7*24*60*60)
