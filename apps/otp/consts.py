from django.db import models
from django.utils.translation import gettext_lazy as _

DEFAULT_OTP_LENGTH = 6

MAX_OTP_FAILURE = 5


class OTPPurpose(models.TextChoices):
    LOGIN_CUSTOMER = "LOGIN_CUSTOMER", _("Login Customer")
    SIGNUP_CUSTOMER = "SIGNUP_CUSTOMER", _("SingUp Customer")
