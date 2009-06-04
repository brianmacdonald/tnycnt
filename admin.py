from django.contrib import admin
from models import Contact

class ContactAdmin(admin.ModelAdmin):
        list_display=('title',)
        list_per_page = 25
        search_fields = ['title','hash']

admin.site.register(Contact, ContactAdmin)