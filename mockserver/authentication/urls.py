from django.urls import path

from authentication.views import (
    Login,
    Logout,
    PasswordResetRequest,
    PasswordReset,
    PasswordChange
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
    path(
        'password-change',
        PasswordChange.as_view({'post': 'create'}),
        name='password_change'
    ),
]
