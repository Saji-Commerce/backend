from django.db import models

from apps.offers.consts import ShippingMethod


class OfferFulfillment(models.Model):
    offer = models.ForeignKey(
        "offers.Offer",
        on_delete=models.CASCADE,
    )
    method = models.CharField(
        max_length=20,
        choices=ShippingMethod.choices,
    )
    is_enabled = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    preparation_time_hours = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("offer", "method"),
                name="unique_offer_shipping_method",
            )
        ]
