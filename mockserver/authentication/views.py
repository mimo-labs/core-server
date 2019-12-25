import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, viewsets, status

from authentication.models import User
from authentication.serializers import LoginSerializer


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
