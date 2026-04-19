from core.views import catalog_page, product_detail


def build_catalog_index(catalog_key: str):
    def view(request):
        return catalog_page(request, catalog_key)

    return view


def build_catalog_detail(catalog_key: str):
    def view(request, product_id):
        return product_detail(request, catalog_key, product_id)

    return view
