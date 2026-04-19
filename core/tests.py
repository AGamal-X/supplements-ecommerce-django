from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.cart import get_cart_summary
from payment.models import Order
from shop.models import Product, ProductCategory


class StorefrontSmokeTests(TestCase):
    def test_home_about_contact_and_shop_pages_render(self):
        for url in [reverse('home'), reverse('about'), reverse('contact'), reverse('shop')]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_unified_shop_category_filter_renders(self):
        Product.objects.create(
            id='greens-1',
            category=ProductCategory.GREENS,
            name='Green Mix',
            price='100',
            details='daily greens',
            description='desc',
        )
        response = self.client.get(reverse('shop'), {'category': ProductCategory.GREENS})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Green Superfood')
        self.assertContains(response, 'Green Mix')

    def test_add_to_cart_and_checkout_creates_order(self):
        User.objects.create_user(username='tester', password='pass12345', email='tester@example.com')
        product = Product.objects.create(
            id='performance-1',
            category=ProductCategory.PERFORMANCE,
            name='Test Product',
            price='100',
            details='details',
            description='desc',
        )
        add_response = self.client.post(reverse('add_to_cart', args=['shop', product.pk]), {'quantity': 2}, follow=True)
        self.assertEqual(add_response.status_code, 200)
        summary = get_cart_summary(self.client.session)
        self.assertEqual(summary['item_count'], 2)

        self.client.login(username='tester', password='pass12345')
        checkout_response = self.client.post(reverse('payment'), {
            'full_name': 'Test User',
            'email': 'tester@example.com',
            'phone': '01000000000',
            'address': 'Giza',
            'city': 'Cairo',
            'payment_method': 'cod',
            'notes': 'Leave at the door',
        }, follow=True)
        self.assertEqual(checkout_response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)

    def test_sign_up_creates_user(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser', email='new@example.com').exists())


    def test_profile_requires_login_then_renders_for_user(self):
        user = User.objects.create_user(username='profileuser', password='StrongPass123', email='profile@example.com')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='profileuser', password='StrongPass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'profile@example.com')


    def test_navigation_and_home_ui_elements_render(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Shop supplements')
        self.assertContains(response, 'Fuel your goals')
        self.assertContains(response, 'cart-icon-link')

    def test_shop_search_suggestions_returns_matches(self):
        Product.objects.create(
            id='protein-bars-99',
            category=ProductCategory.PROTEIN_BARS,
            name='Protein Cookie Bar',
            price='90',
            details='portable bar',
            description='snack',
        )
        response = self.client.get(reverse('shop_search_suggestions'), {'q': 'Prot'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Protein Cookie Bar')
