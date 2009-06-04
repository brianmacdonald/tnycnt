from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^new/$', 'tnycnt.views.new_form', name='tnycnt_new'),
    url(r'^forms/', 'tnycnt.views.list_forms', name='tnycnt_list'), 
    url(r'^edit/(?P<form_id>\w+)/$', 'tnycnt.views.edit_form', name='tnycnt_edit'),
    url(r'^sent/$', direct_to_template, {'template': 'tnycnt/tnycnt_sent.html'}, name='tnycnt_sent'),      
	url(r'^(?P<hash>\w+)/$', 'tnycnt.views.view_form', name='tnycnt_mailform'),    	
    )