from django.contrib.auth import get_user_model
from django.db import models

from utils.models import CreateTracker, UUIDPrimaryKey

User = get_user_model()


class CustomerAddress(UUIDPrimaryKey, CreateTracker):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    label = models.CharField(
        max_length=100,
    )
    province = models.CharField(
        max_length=100,
    )
    city = models.CharField(
        max_length=100,
    )
    address = models.TextField()
    house_number = models.CharField(
        max_length=50,
    )
    building_unit = models.CharField(
        max_length=50,
        blank=True,
    )
    postal_code = models.CharField(
        max_length=20,
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
    )
    receiver_full_name = models.CharField(
        max_length=255,
    )
    receiver_phone_number = models.CharField(
        max_length=20,
    )

    class Meta(CreateTracker.Meta):
        pass
