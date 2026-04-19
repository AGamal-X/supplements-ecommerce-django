from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.cart import add_to_cart, clear_cart, get_cart_summary, remove_from_cart, update_quantity
from core.catalog import CATALOG, get_catalog_config, get_catalog_queryset, get_model, get_shop_categories, get_shop_category_label
from core.forms import CheckoutForm, SignInForm, SignUpForm
from core.services import create_order_from_summary
from core.theme import template_path
from payment.models import Order


def catalog_page(request, catalog_key: str, featured_only: int | None = None):
    if catalog_key not in CATALOG:
        raise Http404('Catalog not found')

    queryset, config = get_catalog_queryset(catalog_key)
    selected_category = request.GET.get('category', '').strip()
    search_term = request.GET.get('q', '').strip()

    if catalog_key == 'shop' and selected_category:
        queryset = queryset.filter(category=selected_category)
    if search_term:
        queryset = queryset.filter(name__icontains=search_term)

    products = list(queryset)
    if featured_only is not None:
        products = products[:featured_only]

    category_name = get_shop_category_label(selected_category) if selected_category else config.label
    return render(request, template_path('catalog_list.html'), {
        'catalog_key': catalog_key,
        'category_name': category_name,
        'products': products,
        'search_term': search_term,
        'detail_route_name': config.detail_route_name,
        'shop_categories': get_shop_categories() if catalog_key == 'shop' else [],
        'selected_category': selected_category,
        'search_suggestions_url': 'shop_search_suggestions',
    })


def product_detail(request, catalog_key: str, product_id):
    if catalog_key not in CATALOG:
        raise Http404('Catalog not found')
    config = get_catalog_config(catalog_key)
    model = get_model(config.model)
    product = get_object_or_404(model, pk=product_id)
    category_name = getattr(product, 'category_label', config.label)
    return render(request, template_path('product_detail.html'), {
        'product': product,
        'category_name': category_name,
        'catalog_key': catalog_key,
        'detail_route_name': config.detail_route_name,
    })


@require_POST
def add_product_to_cart(request, catalog_key: str, product_id):
    add_to_cart(request.session, catalog_key, product_id, quantity=request.POST.get('quantity', 1))
    messages.success(request, 'Product added to cart.')
    return redirect(request.POST.get('next') or 'shoppingcart')


@require_POST
def cart_update(request):
    item_key = request.POST.get('item_key', '')
    action = request.POST.get('action')
    if action == 'remove':
        remove_from_cart(request.session, item_key)
        messages.info(request, 'Item removed from cart.')
    else:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        update_quantity(request.session, item_key, quantity)
        messages.success(request, 'Cart updated.')
    return redirect('shoppingcart')


def cart_view(request):
    return render(request, template_path('cart.html'))


@login_required
def checkout_view(request):
    summary = get_cart_summary(request.session)
    initial = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
    }
    form = CheckoutForm(request.POST or None, initial=initial)
    order_placed = None

    if request.method == 'POST':
        if not summary['items']:
            messages.error(request, 'Your cart is empty.')
            return redirect('shoppingcart')
        if form.is_valid():
            order_placed = create_order_from_summary(user=request.user, form_data=form.cleaned_data, summary=summary)
            clear_cart(request.session)
            summary = get_cart_summary(request.session)
            form = CheckoutForm(initial=initial)
            messages.success(request, f'Order #{order_placed.pk} placed successfully.')

    return render(request, template_path('checkout.html'), {
        'form': form,
        'cart_summary': summary,
        'order_placed': order_placed,
    })


def signin_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignInForm(request, data=request.POST or None)
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Signed in successfully.')
        return redirect(next_url)
    return render(request, template_path('signin.html'), {'form': form, 'next_url': next_url})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account has been created.')
        return redirect('home')
    return render(request, template_path('signup.html'), {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('home')


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')[:10]
    return render(request, template_path('profile.html'), {
        'orders': orders,
    })


@require_GET
def shop_search_suggestions(request):
    search_term = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    queryset, _ = get_catalog_queryset('shop')
    if selected_category:
        queryset = queryset.filter(category=selected_category)
    if not search_term:
        return JsonResponse({'results': []})
    queryset = queryset.filter(name__icontains=search_term)[:6]
    config = get_catalog_config('shop')
    results = [
        {
            'id': str(product.pk),
            'name': product.name,
            'price': str(product.price),
            'category': getattr(product, 'category_label', 'Shop'),
            'url': reverse(config.detail_route_name, args=[product.pk]),
        }
        for product in queryset
    ]
    return JsonResponse({'results': results})
