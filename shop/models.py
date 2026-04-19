from django.db import models

from core.product_models import BaseProductModel


class ProductCategory(models.TextChoices):
    PERFORMANCE = 'performance', 'Performance Essentials'
    GREENS = 'greens', 'Green Superfood'
    MUSCLE = 'muscle', 'Muscle Building Supplements'
    PEANUT_BUTTER = 'peanut-butter', 'Peanut Butter'
    PROTEIN_BARS = 'protein-bars', 'Protein Bars'
    WEIGHT_LOSS = 'weight-loss', 'Weight Loss'


class Product(BaseProductModel):
    id = models.CharField(max_length=40, primary_key=True)
    category = models.CharField(max_length=30, choices=ProductCategory.choices, default=ProductCategory.PERFORMANCE)
    name = models.CharField(max_length=255)
    price = models.TextField()
    details = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    @property
    def category_label(self) -> str:
        return self.get_category_display()
