from django.db import models

from apps.catalogs.consts import SpecificationValueType


class SpecificationGroup(models.Model):
    name = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Specification(models.Model):
    group = models.ForeignKey(
        SpecificationGroup,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    value_type = models.CharField(max_length=30, choices=SpecificationValueType.choices)
    unit = models.CharField(max_length=50, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class SpecificationOption(models.Model):
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "value"]


class CategorySpecification(models.Model):
    category = models.ForeignKey(
        "catalogs.Category",
        on_delete=models.CASCADE,
    )
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
    )
    required = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "specification"],
                name="unique_category_specification",
            )
        ]
