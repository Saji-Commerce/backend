from django.db import models

from utils.models import CreateUpdateTracker, UUIDPrimaryKey


class Offer(UUIDPrimaryKey, CreateUpdateTracker):
    store = models.ForeignKey(
        "sellers.StoreProfile",
        on_delete=models.CASCADE,
    )
    variant = models.ForeignKey(
        "catalogs.ProductVariant",
        on_delete=models.PROTECT,
    )
    price = models.PositiveBigIntegerField()
    max_quantity_per_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("store", "variant"),
                name="unique_store_variant_offer",
            )
        ]
