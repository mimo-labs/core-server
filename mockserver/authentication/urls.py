from django.urls import path

from authentication.views import (
    Login,
    Logout,
    PasswordResetRequest,
    PasswordReset,
)

urlpatterns = [
    path(
        'login',
        Login.as_view({'post': 'create'}),
        name='login'
    ),
    path(
        'logout',
        Logout.as_view({'post': 'create'}),
        name='logout'
    ),
    path(
        'password-reset-request',
        PasswordResetRequest.as_view({'post': 'create'}),
        name='password_reset_request'
    ),
    path(
        'password-reset',
        PasswordReset.as_view({'post': 'create'}),
        name='password_reset'
    ),
]
