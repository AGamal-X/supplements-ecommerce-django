from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from importlib import import_module

from shop.models import ProductCategory


@dataclass(frozen=True)
class CatalogConfig:
    key: str
    model: str
    label: str
    route_name: str
    detail_route_name: str


CATALOG = {
    'home': CatalogConfig('home', 'shop.models.Product', 'Featured Products', 'home', 'shop_detail'),
    'shop': CatalogConfig('shop', 'shop.models.Product', 'Shop', 'shop', 'shop_detail'),
}

SHOP_CATEGORY_KEYS = [choice[0] for choice in ProductCategory.choices]
SHOP_CATEGORY_LABELS = dict(ProductCategory.choices)


def get_model(path: str):
    module_name, class_name = path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, class_name)


def get_catalog_config(key: str) -> CatalogConfig:
    return CATALOG[key]


def get_catalog_queryset(key: str):
    config = get_catalog_config(key)
    model = get_model(config.model)
    return model.objects.all(), config


def get_shop_categories():
    return [{'key': key, 'label': SHOP_CATEGORY_LABELS[key]} for key in SHOP_CATEGORY_KEYS]


def get_shop_category_label(category_key: str) -> str:
    return SHOP_CATEGORY_LABELS.get(category_key, 'Shop')


def parse_price(value) -> Decimal:
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError, AttributeError):
        return Decimal('0.00')
