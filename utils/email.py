from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from utils.email_templates import EmailTemplates


class Email:
    
    @staticmethod
    @shared_task
    def send_server_error(error):
        send_mail(
            f'Jasiri Wallet | {settings.SERVER} Server Error',
            error,
            settings.COMPANY_EMAIL,
            [settings.DEV_EMAIL],
            fail_silently=False,
        )


    @staticmethod
    def send_verify_asset_mail(url, title_id, email):
        url = settings.ALLOWED_HOSTS[0] + url
        try:
            send_mail(
                subject= f'Jasiri Console Verify Titles',
                html_message=EmailTemplates.title_verify(url,title_id),
                message="Vefify Titles",
                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
                )
        except:
            pass