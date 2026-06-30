from django.contrib.auth import get_user_model
from django.db import models

from utils.models import CreateTracker, UUIDPrimaryKey

User = get_user_model()


class StoreAddress(UUIDPrimaryKey, CreateTracker):
    store = models.ForeignKey(
        "sellers.StoreProfile",
        on_delete=models.CASCADE,
    )
    province = models.CharField(
        max_length=100,
    )
    city = models.CharField(
        max_length=100,
    )
    address = models.TextField()
    plaque = models.CharField(
        max_length=20,
        blank=True,
    )
    postal_code = models.CharField(
        max_length=20,
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    class Meta(CreateTracker.Meta):
        pass
