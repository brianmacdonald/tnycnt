"""
Views allow users to view/send, create and edit contact forms.

"""

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from models import Contact
from forms import ContactForm, ContactMailForm

try:
    from recaptcha.client import captcha
except ImportError:
    raise ImportError, 'Please install reCAPTCHA clinet. See http://pypi.python.org/pypi/recaptcha-client.' 

try:
    from settings import RECAPTCHA_PRIVATE_KEY
    from settings import RECAPTCHA_PUB_KEY
except ImportError:
    raise ImportError, 'Please enter valid reCAPTCHA api private and public keys in the projects settings file.'

def view_form(request, hash, not_active_template = 'tnycnt/tnycnt_not_active.html', 
              form_template = 'tnycnt/tnycnt_mailform.html',
              message_template = 'tnycnt/tnycnt_message.txt',
              ):
    """
    View and send a user created contact form.
    Uses recaptcha lib. If captcha is wrong a message is shown above form.  
    Mail message body can be edit in 'tnycnt/tnycnt_message.txt' and the message
    subject needs TNYCNT_MAIL_SUBJECT in settings file.
    """
    object = get_object_or_404(Contact, hash=hash)
    message = '' 
    if object.is_active == False:
        return render_to_response(not_active_template,
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        # Captcha check
        check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'],
                        request.POST['recaptcha_response_field'],
                        RECAPTCHA_PRIVATE_KEY,
                        request.META['REMOTE_ADDR'])
        form = ContactMailForm(request.POST)
        html_captcha = captcha.displayhtml(RECAPTCHA_PUB_KEY)
        if check_captcha.is_valid is False:
            #captcha is wrong
            message = _('Captcha failed')
        else:    
            if form.is_valid():
                from django.core.mail import send_mail		
                current_site = Site.objects.get_current()            
                subject = settings.TNYCNT_MAIL_SUBJECT        
                message = render_to_string(message_template,
                                           {'site_name':current_site,
                                            'title':object.title,
                                            'subject':form.cleaned_data['subject'],
                                            'email':form.cleaned_data['email'],
                                            'body': form.cleaned_data['body'] })            
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                          [object.user.email])
                return HttpResponseRedirect(reverse('tnycnt_sent'))
    else:
        form = ContactMailForm()
        html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    return render_to_response(form_template,
                             {'form': form,
                              'html_captcha': html_captcha,
                              'object':object,
                              'message':message},
                              context_instance=RequestContext(request))

def list_forms(request, template_name = 'tnycnt/tnycnt_list.html'):
    """
    Display user created contact forms in reverse chronological order
    """
    domain = Site.objects.get_current().domain
    object_list = Contact.objects.filter(user=request.user).order_by("-created_at")
    return render_to_response(template_name, {
                              'object_list': object_list, 'domain': domain,
                              },
                              context_instance=RequestContext(request)
                              )
list_forms = login_required(list_forms)
    
def new_form(request, template_name = 'tnycnt/tnycnt_edit.html'):
    """
    Create new user created contact form
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contactform = form.save(commit=False)
            contactform.user = request.user
            contactform.save()
            return HttpResponseRedirect(reverse("tnycnt_list"))    
    else:
        form = ContactForm()
        status = _("Create")
    return render_to_response(template_name, {
                              'form': form, 'status': status,
                              },
                              context_instance=RequestContext(request)
                              )                                     
new_form = login_required(new_form)
    
def edit_form(request,form_id, template_name = 'tnycnt/tnycnt_edit.html'):
    """
    Edit user created contact form
    """
    userform = get_object_or_404(Contact, id=form_id)
    if userform.user != request.user:
        return HttpResponseRedirect('/404/')
    if request.method == "POST":
        form = ContactForm(request.POST, instance=userform)
        if form.is_valid():
            contactform = form.save(commit=False)
            contactform.user = request.user
            contactform.save()
            return HttpResponseRedirect(reverse("tnycnt_list"))    
    else:
        form = ContactForm(instance=userform)
        status = _("Edit")
    return render_to_response(template_name, {
                              'form': form, 'status': status,
                              },
                              context_instance=RequestContext(request)
                              )   
edit_form = login_required(edit_form)
	
