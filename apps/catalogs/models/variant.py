from django.db import models


class VariantGroup(models.Model):
    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.name


class Variant(models.Model):
    variant_group = models.ForeignKey(
        VariantGroup,
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=255)
    display_value = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "value"]

    def __str__(self):
        return self.display_value


class CategoryVariantGroup(models.Model):
    category = models.ForeignKey(
        "catalogs.Category",
        on_delete=models.CASCADE,
    )
    variant_group = models.ForeignKey(
        VariantGroup,
        on_delete=models.CASCADE,
    )
    required = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "variant_group"],
                name="unique_category_variant_group",
            )
        ]
