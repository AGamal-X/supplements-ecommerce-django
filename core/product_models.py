from __future__ import annotations

from decimal import Decimal, InvalidOperation

from django.db import models
from django.utils.html import format_html


class BaseProductModel(models.Model):
    """Common product behavior shared by the storefront catalogs.

    Keeping this abstract lets the project preserve the current database schema
    while removing duplicated model helpers from each catalog app.
    """

    image = models.ImageField(upload_to='static/images/', blank=True)

    class Meta:
        abstract = True

    @property
    def parsed_price(self) -> Decimal:
        try:
            return Decimal(str(getattr(self, "price", 0)).strip())
        except (InvalidOperation, AttributeError, ValueError):
            return Decimal('0.00')

    @property
    def short_description(self) -> str:
        return getattr(self, "description", "") or getattr(self, "details", "") or ""

    @property
    def image_url(self) -> str:
        if not self.image:
            return ''
        try:
            return self.image.url
        except ValueError:
            return ''

    def image_tag(self):
        if not self.image_url:
            return 'No image'
        return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;" />', self.image_url)

    image_tag.short_description = 'Preview'
