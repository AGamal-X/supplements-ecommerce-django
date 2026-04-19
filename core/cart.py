from dataclasses import dataclass
from decimal import Decimal
from typing import List
from django.urls import reverse
from core.catalog import CATALOG, get_model, parse_price

CART_SESSION_KEY = 'cart'


@dataclass
class CartItem:
    key: str
    app_label: str
    product_id: str
    name: str
    price: Decimal
    quantity: int
    image_url: str
    detail_url: str
    line_total: Decimal


def _get_cart_store(session):
    return session.setdefault(CART_SESSION_KEY, {})


def make_cart_key(app_label: str, product_id) -> str:
    return f'{app_label}:{product_id}'


def add_to_cart(session, app_label: str, product_id, quantity: int = 1):
    store = _get_cart_store(session)
    key = make_cart_key(app_label, product_id)
    store[key] = store.get(key, 0) + max(1, int(quantity))
    session.modified = True


def update_quantity(session, item_key: str, quantity: int):
    store = _get_cart_store(session)
    if quantity <= 0:
        store.pop(item_key, None)
    elif item_key in store:
        store[item_key] = int(quantity)
    session.modified = True


def remove_from_cart(session, item_key: str):
    store = _get_cart_store(session)
    if item_key in store:
        store.pop(item_key, None)
        session.modified = True


def clear_cart(session):
    if CART_SESSION_KEY in session:
        session[CART_SESSION_KEY] = {}
        session.modified = True


def get_cart_items(session) -> List[CartItem]:
    store = session.get(CART_SESSION_KEY, {})
    items: List[CartItem] = []
    for key, quantity in store.items():
        try:
            app_label, product_id = key.split(':', 1)
            config = CATALOG[app_label]
            model = get_model(config.model)
            product = model.objects.get(pk=product_id)
            price = parse_price(getattr(product, 'price', 0))
            detail_url = reverse(config.detail_route_name, args=[product.pk])
            image_field = getattr(product, 'image', None)
            image_url = image_field.url if image_field else ''
            items.append(CartItem(
                key=key,
                app_label=app_label,
                product_id=str(product.pk),
                name=getattr(product, 'name', 'Product'),
                price=price,
                quantity=int(quantity),
                image_url=image_url,
                detail_url=detail_url,
                line_total=price * int(quantity),
            ))
        except Exception:
            continue
    return items


def get_cart_summary(session):
    items = get_cart_items(session)
    subtotal = sum((item.line_total for item in items), Decimal('0.00'))
    shipping = Decimal('0.00') if not items or subtotal >= Decimal('500') else Decimal('50.00')
    total = subtotal + shipping
    return {
        'items': items,
        'item_count': sum(item.quantity for item in items),
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
