import logging

from celery.task import task

from tenants.invites.strategy import UserMailingStrategy


logger = logging.getLogger(__name__)


@task()
def mail_membership_invite(is_existing, invite_email, organization_name, from_domain):
    logger.info(f"sending org {organization_name} invite is_existing {is_existing}")
    mailing = UserMailingStrategy.get_strategy(is_existing)
    mailing.generate_invite(invite_email, organization_name, from_domain)
