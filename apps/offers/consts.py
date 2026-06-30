from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ShippingMethod(TextChoices):
    SELLER = "SELLER", _("Seller Shipping")
    PLATFORM = "PLATFORM", _("Platform Shipping")
