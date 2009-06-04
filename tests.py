"""
More tests need to be written
"""

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
                                      user=self.sample_user,)
        self.sample_contact_form.save()                              
                                      
class TnycntModelTests(TnycntTestCase): 

    def test_hash_creation_check(self):
        """
        Test if hash was created.        
        """
        self.failUnless(self.sample_contact_form.hash)                                     
                                      
        
       