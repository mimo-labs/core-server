import logging
from smtplib import SMTPException

from django.contrib.auth import (
    authenticate,
    get_user_model
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import (
    JsonResponse,
    HttpResponse
)
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, viewsets, status
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE
)

from authentication import constants
from authentication.models import User
from authentication.serializers import (
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer
)


logger = logging.getLogger(__name__)


class Login(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ Login user """

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(**serializer.data)
            if not user:
                raise PermissionDenied()

            user = User.objects.get(email=serializer.validated_data['email'])
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token = Token.objects.get(user=user)

            return JsonResponse({'token': token.key, 'id': user.id})
        except (ObjectDoesNotExist, PermissionDenied, ValidationError) as e:
            logger.warning(e)
            return JsonResponse(
                {'detail': 'invalid username or password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(e)
            return JsonResponse(
                {'detail': 'unexpected error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Logout(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return JsonResponse({'detail': 'account logged out successfully'})


class PasswordResetRequest(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        logger.info(f'password reset request user {request.data["email"]}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_model = get_user_model()

        try:
            user = user_model.objects.get(
                email=serializer.validated_data['email']
            )
        except user_model.DoesNotExist:
            logger.info(f'user {request.data["email"]} does not exist')
            return JsonResponse({'detail': 'user does not exist'}, status=HTTP_404_NOT_FOUND)
        new_token, _ = Token.objects.get_or_create(user=user)

        # TODO: define front-end url, mail format
        # TODO: Set up celery and message queue to send mails async
        try:
            send_mail(
                constants.PASSWORD_RESET_MAIL_SUBJECT,
                constants.PASSWORD_RESET_MESSAGE_BODY,
                constants.PASSWORD_RESET_MAIL_SENDER,
                (request.data['email'],),
                fail_silently=False
            )
        except SMTPException as exc:
            logger.error(f'send mail error: {exc}')
            return JsonResponse({'detail': str(exc).lower()}, status=HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as exc:
            logger.exception(exc)
            raise
        logger.info(f'reset mail sent user {request.data["email"]}')
        return HttpResponse('', status=HTTP_204_NO_CONTENT)


class PasswordReset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        logger.info(f'password reset user {request.user.email}')
        # TODO: I don't like this. Instead of using an API token we should
        # generate a one-off token elsewhere and validate it. This is a potential
        # security issue
        Token.objects.filter(user=request.user).delete()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(f'reset OK user {request.user.email}')
        return HttpResponse('', status=HTTP_204_NO_CONTENT)


class PasswordChange(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        logger.info(f'password change user {request.user.email}')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(f'change OK user {request.user.email}')
        return HttpResponse('', status=HTTP_204_NO_CONTENT)
