from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

DEFAULT_OTP_LENGTH = 6

MAX_OTP_FAILURE = 5


class OTPPurpose(TextChoices):
    LOGIN_CUSTOMER = "LOGIN_CUSTOMER", _("Login Customer")
    SIGNUP_CUSTOMER = "SIGNUP_CUSTOMER", _("SingUp Customer")
    LOGIN_SELLER = "LOGIN_SELLER", _("Login Seller")
    SIGNUP_SELLER = "SIGNUP_SELLER", _("SingUp Seller")
