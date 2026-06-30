from enum import StrEnum

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AccountType(TextChoices):
    CUSTOMER = "CUSTOMER", _("Customer")
    SELLER = "SELLER", _("Seller")
    STAFF = "STAFF", _("Staff")


class AuthStep(StrEnum):
    OTP = "OTP"
    PASSWORD = "PASSWORD"
