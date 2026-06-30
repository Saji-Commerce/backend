from django.contrib.auth import get_user_model
from django.db import models

from utils.models import CreateUpdateTracker, UUIDPrimaryKey

User = get_user_model()


class SellerProfile(UUIDPrimaryKey, CreateUpdateTracker):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
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
        unique=True,
    )
    email = models.EmailField(
        blank=True,
    )
