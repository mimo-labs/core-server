import logging

from django.contrib.auth import (
    authenticate,
    get_user_model
)
from rest_framework.settings import api_settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    JsonResponse,
    HttpResponse
)
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, viewsets, status, views
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from authentication.backends import MailingTokenAuthentication
from authentication.models import (
    User,
    OneOffToken
)
from authentication.serializers import (
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer
)
from authentication.tasks import mail_reset_request


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


class Logout(views.APIView):
    def post(self, request):
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
        new_token, _ = OneOffToken.objects.get_or_create(user=user)

        # TODO: define front-end url, mail format
        mail_reset_request.delay(request.data['email'], new_token.key)
        logger.info(f'reset mail sent user {request.data["email"]}')
        return HttpResponse('', status=HTTP_204_NO_CONTENT)


class PasswordReset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (
        MailingTokenAuthentication,
        *api_settings.DEFAULT_AUTHENTICATION_CLASSES
    )
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        logger.info(f'password reset user {request.user.email}')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(f'reset OK user {request.user.email}')
        return HttpResponse('', status=HTTP_204_NO_CONTENT)
