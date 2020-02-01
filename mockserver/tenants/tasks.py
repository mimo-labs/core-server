import logging

from celery.task import task

from tenants.invites.strategy import UserMailingStrategy


logger = logging.getLogger(__name__)


@task()
def mail_membership_invite(invite):
    is_existing = invite.tenant is not None
    logger.info(f"sending org f{invite.organization.name} invite is_existing {is_existing}")
    mailing = UserMailingStrategy.get_strategy(is_existing)
    mailing.generate_invite(invite.email, invite.organization.name)
