from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from apps.accounts.consts import AccountType
from utils.models import CreateUpdateTracker, UUIDPrimaryKey


class User(UUIDPrimaryKey, CreateUpdateTracker, AbstractBaseUser):
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
    )
    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = "phone_number"

    class Meta:
        indexes = [
            models.Index(
                fields=["phone_number", "account_type"],
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number", "account_type"],
                name="unique_user_per_phone_number_and_account_type",
            )
        ]
