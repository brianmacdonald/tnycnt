from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Contact

class ContactForm(forms.ModelForm):
    """
    Model Form for for creating and editing 
    user created contact forms
    """
    class Meta:
        model = Contact
        fields = (
                  'title', 
                  'description',
                  'is_active',
                  )
                  
class ContactMailForm(forms.Form):
    """
    Form to send messages
    """
    email = forms.EmailField(label=_('Email'))
    subject = forms.CharField(max_length=255, label=_('Subject'))
    body = forms.CharField(max_length=512,widget=forms.widgets.Textarea(), label=_('Body'))