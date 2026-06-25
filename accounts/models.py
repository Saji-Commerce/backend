from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from accounts.consts import AccountType
from utils.models import CreateUpdateTracker, UUIDPrimaryKey


class User(UUIDPrimaryKey, CreateUpdateTracker, AbstractBaseUser):
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
    )
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
    )
    is_active = models.BooleanField(
        default=True,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
