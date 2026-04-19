from core.cart import get_cart_summary
from core.theme import get_theme


def storefront(request):
    return {
        'cart_summary': get_cart_summary(getattr(request, 'session', {})),
        'ui_theme': get_theme(request),
    }
