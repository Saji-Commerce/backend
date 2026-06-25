from django.db import models

from apps.otp.consts import OTPPurpose
from utils.models import CreateTracker


class OTP(CreateTracker):
    identifier = models.CharField(
        max_length=255,
    )
    purpose = models.CharField(
        max_length=50,
        choices=OTPPurpose.choices,
    )
    code = models.CharField(
        max_length=255,
    )
    is_used = models.BooleanField(
        default=False,
    )
    failed_attempts = models.PositiveSmallIntegerField(
        default=0,
    )
    expires_at = models.DateTimeField()

    class Meta(CreateTracker.Meta):
        indexes = [
            models.Index(
                fields=["identifier", "purpose"],
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "purpose"],
                condition=models.Q(is_used=False),
                name="unique_active_otp_per_identifier_and_purpose",
            )
        ]
