from datetime import datetime
from hashlib import md5

from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _

import random

class Contact(models.Model):
    """ 
    Model for User created contact forms. 
    hash is created randomly 
    """
    title       = models.CharField(_('Title'),max_length=255,)
    description = models.TextField(_('Description'), null=True)
    user        = models.ForeignKey(User)
    hash        = models.CharField(max_length=6, db_index=True, blank=True, unique=True, default=None)
    created_at  = models.DateTimeField(_('Created at'), default=datetime.now)
    is_active   = models.BooleanField(_('Active'), default=False)
    
    def save(self, **kw):
        if self.hash == None:
            self.hash = md5(str(random.randint(1,99999))).hexdigest()[:4]
        try:
            super(Contact, self).save(**kw)
        #hash already exist
        #small chance of happening but just in case
        except IntegrityError:
            match_obj = re.match(r'^(.*)+(\d+)$', self.slug)
            if match_obj:
                next_int = int(match_obj.group(2)) + 1
                self.slug = match_obj.group(1) + '+' + str(next_int)
            else:
                self.slug += '+2'        
             

    def get_absolute_url(self):
        return '/%s/' % self.hash
