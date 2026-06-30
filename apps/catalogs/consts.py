from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProductState(TextChoices):
    INITIALIZE = "INITIALIZE", _("Initialize")
    READY_TO_PUBLISH = "READY_TO_PUBLISH", _("Ready to publish")
    UNDER_REVIEW = "UNDER_REVIEW", _("Under review")
    NEED_EDIT = "NEED_EDIT", _("Need editing")
    APPROVED = "APPROVED", _("Approved")


class SpecificationValueType(TextChoices):
    TEXT = "TEXT", _("Text")
    LONG_TEXT = "LONG_TEXT", _("Long Text")
    INTEGER = "INTEGER", _("Integer")
    DECIMAL = "DECIMAL", _("Decimal")
    BOOLEAN = "BOOLEAN", _("Boolean")
    SELECT = "SELECT", _("Select")
    MULTI_SELECT = "MULTI_SELECT", _("Multi Select")
