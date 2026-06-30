from django.contrib.auth import get_user_model
from django.db import models

from utils.models import CreateUpdateTracker, UUIDPrimaryKey

User = get_user_model()


class StoreProfile(UUIDPrimaryKey, CreateUpdateTracker):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
    )
    logo = models.ImageField(
        upload_to="stores/logos/",
        blank=True,
    )
    description = models.TextField(
        blank=True,
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )
    website = models.URLField(
        blank=True,
    )
