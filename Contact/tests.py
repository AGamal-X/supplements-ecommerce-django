from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactFormTests(TestCase):
    def test_contact_submission_is_saved_to_database(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Ahmed Jamal',
            'email': 'ahmed@example.com',
            'message': 'I want to ask about creatine availability.',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)
        saved = Contact.objects.get()
        self.assertEqual(saved.name, 'Ahmed Jamal')
        self.assertEqual(saved.email, 'ahmed@example.com')
