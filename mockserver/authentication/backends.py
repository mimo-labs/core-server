from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header
)

from django.utils.translation import ugettext_lazy as _

from authentication.models import OneOffToken


class MailingTokenAuthentication(BaseAuthentication):
    model = OneOffToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower().decode() != 'mailtoken':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = self.model.objects.select_related("user").get(key=token)

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        token.delete()

        return token.user, None
