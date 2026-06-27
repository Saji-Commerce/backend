from django.contrib.auth import get_user_model
from django.db import models

from utils.models import CreateUpdateTracker, UUIDPrimaryKey

User = get_user_model()


class CustomerProfile(UUIDPrimaryKey, CreateUpdateTracker):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
    )
    national_code = models.CharField(
        max_length=20,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
