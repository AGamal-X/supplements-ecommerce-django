from django.shortcuts import render

from core.catalog import get_catalog_queryset
from core.catalog_views import build_catalog_detail
from core.theme import template_path


def index(request):
    queryset, _ = get_catalog_queryset('shop')
    products = list(queryset[:6])
    return render(request, template_path('home.html'), {
        'products': products,
        'catalog_key': 'shop',
        'detail_route_name': 'shop_detail',
    })


home_detail = build_catalog_detail('shop')
