import logging
from smtplib import SMTPException

from celery.task import task
from django.core.mail import send_mail

from authentication import constants


logger = logging.getLogger(__name__)


@task()
def mail_reset_request(email: str, token: str):
    logger.info(f'mailing {email} for password reset')
    try:
        send_mail(
            constants.PASSWORD_RESET_MAIL_SUBJECT,
            constants.PASSWORD_RESET_MESSAGE_BODY,
            constants.PASSWORD_RESET_MAIL_SENDER,
            (email,),
            fail_silently=False
        )
    except SMTPException as exc:
        logger.error(f'send mail error: {exc}')
    except Exception as exc:
        logger.exception(exc)
