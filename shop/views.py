from core.catalog_views import build_catalog_detail, build_catalog_index
from core.views import shop_search_suggestions


index = build_catalog_index('shop')
shop_detail = build_catalog_detail('shop')
search_suggestions = shop_search_suggestions
