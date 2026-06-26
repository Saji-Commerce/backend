from django.urls import path

from apps.accounts.consts import AccountType
from apps.accounts.views import AuthPasswordLoginView, AuthStartView, AuthVerifyOTPView

urlpatterns = [
    path(
        "customer/auth/start/",
        AuthStartView.as_view(account_type=AccountType.CUSTOMER),
        name="customer-auth-start",
    ),
    path(
        "customer/auth/password/",
        AuthPasswordLoginView.as_view(account_type=AccountType.CUSTOMER),
        name="customer-auth-password",
    ),
    path(
        "customer/auth/verify-otp/",
        AuthVerifyOTPView.as_view(account_type=AccountType.CUSTOMER),
        name="customer-auth-verify-otp",
    ),
    path(
        "seller/auth/start/",
        AuthStartView.as_view(account_type=AccountType.SELLER),
        name="seller-auth-start",
    ),
    path(
        "seller/auth/password/",
        AuthPasswordLoginView.as_view(account_type=AccountType.SELLER),
        name="seller-auth-password",
    ),
    path(
        "seller/auth/verify-otp/",
        AuthVerifyOTPView.as_view(account_type=AccountType.SELLER),
        name="seller-auth-verify-otp",
    ),
]
