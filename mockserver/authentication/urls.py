from rest_framework import routers

from authentication.views import (
    Login,
    Logout,
    PasswordResetRequest,
    PasswordReset,
    PasswordChange
)

router = routers.SimpleRouter(trailing_slash=False)
router.register(
    r'login',
    Login,
    base_name='login'
)
router.register(
    r'logout',
    Logout,
    base_name='logout'
)
router.register(
    r'password-reset-request',
    PasswordResetRequest,
    base_name='password_reset_request'
)
router.register(
    r'password-reset',
    PasswordReset,
    base_name='password_reset'
)
router.register(
    r'password-change',
    PasswordChange,
    base_name='password_change'
)

urlpatterns = router.urls
