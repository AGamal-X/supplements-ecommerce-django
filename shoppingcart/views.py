from core.views import cart_view


def index(request):
    return cart_view(request)
