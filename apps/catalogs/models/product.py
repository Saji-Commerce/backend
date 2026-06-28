from django.db import models

from apps.catalogs.consts import ProductState
from utils.models import CreateTracker, CreateUpdateTracker, UUIDPrimaryKey


class Product(UUIDPrimaryKey, CreateUpdateTracker):
    category = models.ForeignKey(
        "catalogs.Category",
        on_delete=models.PROTECT,
    )
    brand = models.ForeignKey(
        "catalogs.Brand",
        on_delete=models.PROTECT,
    )
    persian_name = models.CharField(max_length=300)
    english_name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    introduction = models.TextField(blank=True)
    expert_review = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    length = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    width = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    height = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    state = models.CharField(max_length=30, choices=ProductState.choices)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "persian_name", "english_name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["persian_name", "english_name"]),
        ]

    def __str__(self) -> str:
        return f"{self.persian_name} ({self.english_name})"


class ProductImage(CreateTracker):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="products/images/")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def __str__(self) -> str:
        return f"Image {self.sort_order} for {self.product}"


class ProductVariant(CreateUpdateTracker):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    sku = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.sku


class ProductVariantGroupValue(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
    )
    variant_group = models.ForeignKey(
        "catalogs.VariantGroup",
        on_delete=models.PROTECT,
    )
    variant = models.ForeignKey(
        "catalogs.Variant",
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_variant", "variant_group"],
                name="unique_product_variant_group",
            )
        ]

    def __str__(self) -> str:
        return f"{self.variant} - {self.variant}"


class ProductVariantImage(CreateTracker):
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="variants/images/")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def __str__(self) -> str:
        return f"Image {self.sort_order} for {self.product_variant}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    specification = models.ForeignKey(
        "catalogs.Specification",
        on_delete=models.PROTECT,
    )
    value = models.JSONField()

    class Meta:
        ordering = ["specification"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "specification"],
                name="unique_product_specification",
            )
        ]

    def __str__(self) -> str:
        return f"{self.product} - {self.specification}"
