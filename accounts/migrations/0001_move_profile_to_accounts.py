# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Moving Profile from subscriptions to accounts. 
        db.rename_table('subscriptions_profile', 'accounts_profile')                                                                                                                        
        db.send_create_signal('accounts', ['Profile'])

    def backwards(self, orm):
        # Moving Profile from accounts to subscriptions    
        db.rename_table('accounts_profile', 'subscriptions_profile')                                                                                                                        
        db.send_create_signal('subscriptions', ['Profile'])