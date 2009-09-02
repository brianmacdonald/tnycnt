"""
More tests need to be written
"""

from django.core.urlresolvers import reverse 
from django.core import management
from django.test import TestCase

from models import Contact
from django.contrib.auth.models import User

class TnycntTestCase(TestCase):
    """
    Create a sample contact form
    """
    def setUp(self):
        self.sample_user = User.objects.create_user(username='u', password='p',
                           email='u@example.com')
        self.sample_contact_form = Contact(title='Sample Form',
                                      description='Sample description',
                                      is_active=True,
                                      user=self.sample_user,)
        self.sample_contact_form.save()                              
        self.client.login(username='u', password='p')
                                      
class TnycntModelTests(TnycntTestCase):

    def test_form_creation_check(self):
        """
        Test if form was created.
        """
        self.assertEqual(self.sample_contact_form.pk, 1)

    def test_hash_creation_check(self):
        """
        Test if hash was created.        
        """
        self.failUnless(self.sample_contact_form.hash)                

    def test_single_mailform_view(self):
        """
        Test to see if a single form can be viewed.
        """
        response = self.client.get(reverse('tnycnt_mailform',
                                   args=[],
                                   kwargs={'hash':self.sample_contact_form.hash}))
        self.assertEqual(response.context['object'].pk, 1)
        self.assertEqual(response.status_code, 200)

    def test_list_mailform_view(self):
        """
        Test to see if the list of forms can be viewed.
        """
        response = self.client.get(reverse('tnycnt_list',
                                   args=[],
                                   kwargs={}))
        self.assertEqual(response.context['object_list'].count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_new_mailform_view(self):
        pass

    def test_edit_mailform_view(self):
        pass

    def test_new_mailform_bad_data(self):
        pass

    def test_new_mailform_non_user(self):
        pass

    def test_mailform_edit(self):
        pass

    def test_mailform_delete(self):
        pass

    def test_mailform_send_message(self):
        pass

    def test_mailform_send_message_bad_data(self):
        pass


       
