from typing import Type

from django.core.mail import send_mail

from tenants.invites import constants


class UserMailingStrategy:
    @staticmethod
    def generate_invite(email, organization_name, from_domain):
        raise NotImplementedError()

    @staticmethod
    def get_strategy(is_existing_user: bool) -> Type['UserMailingStrategy']:
        if is_existing_user:
            return RegisterUserUserMailingStrategy
        else:
            return ExistingUserUserMailingStrategy


class RegisterUserUserMailingStrategy(UserMailingStrategy):
    @staticmethod
    def generate_invite(email, organization_name, from_domain):
        # TODO: implement third party smtp
        send_mail(
            constants.INVITE_EMAIL_SUBJECT_FORMAT % organization_name,
            'template goes here',
            None,
            None
        )


class ExistingUserUserMailingStrategy(UserMailingStrategy):
    @staticmethod
    def generate_invite(email, organization_name, from_domain):
        # TODO: implement third party smtp
        send_mail(
            constants.INVITE_EMAIL_SUBJECT_FORMAT % organization_name,
            'template goes here',
            None,
            None
        )
