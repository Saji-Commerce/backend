from django.db import models

from utils.models import CreateTracker


class Brand(CreateTracker):
    persian_name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/")
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["persian_name", "english_name"]

    def __str__(self):
        return f"{self.persian_name} ({self.english_name})"


class CategoryBrand(models.Model):
    category = models.ForeignKey(
        "catalogs.Category",
        on_delete=models.CASCADE,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "brand"],
                name="unique_category_brand",
            )
        ]
