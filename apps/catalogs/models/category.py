from django.db import models
from treebeard.mp_tree import MP_Node


class Category(MP_Node):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    node_order_by = ["sort_order", "name"]

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name
