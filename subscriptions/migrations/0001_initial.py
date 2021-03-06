# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GenericSubscription'
        db.create_table(u'subscriptions_genericsubscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', to=orm['subscriptions.Recipient'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('pretty_name', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('avatar', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('num_borked_calls', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('first_borked_call_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('appears_broken', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'subscriptions', ['GenericSubscription'])

        # Adding model 'Recipient'
        db.create_table(u'subscriptions_recipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipients', to=orm['auth.User'])),
            ('sender_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('sender_phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('add_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('timezone', self.gf('timezone_field.fields.TimeZoneField')()),
            ('language', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=12)),
            ('temperature', self.gf('django.db.models.fields.CharField')(default='F', max_length=1)),
            ('dailywakeup_hour', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('dailywakeup_bucket', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('morning_bucket', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('evening_bucket', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('wee_hours_bucket', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'subscriptions', ['Recipient'])

        # Adding model 'TumblrSubscription'
        db.create_table(u'subscriptions_tumblrsubscription', (
            (u'genericsubscription_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['subscriptions.GenericSubscription'], unique=True, primary_key=True)),
            ('last_post_ts', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'subscriptions', ['TumblrSubscription'])

        # Adding model 'DailyWakeupSubscription'
        db.create_table(u'subscriptions_dailywakeupsubscription', (
            (u'genericsubscription_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['subscriptions.GenericSubscription'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'subscriptions', ['DailyWakeupSubscription'])

        # Adding model 'DailyWakeupContent'
        db.create_table(u'subscriptions_dailywakeupcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')()),
            ('daily_wakeup_subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscriptions.DailyWakeupSubscription'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('subscription_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('subscription_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'subscriptions', ['DailyWakeupContent'])

        # Adding model 'Vacation'
        db.create_table(u'subscriptions_vacation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vacations', to=orm['subscriptions.Recipient'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'subscriptions', ['Vacation'])


    def backwards(self, orm):
        # Deleting model 'GenericSubscription'
        db.delete_table(u'subscriptions_genericsubscription')

        # Deleting model 'Recipient'
        db.delete_table(u'subscriptions_recipient')

        # Deleting model 'TumblrSubscription'
        db.delete_table(u'subscriptions_tumblrsubscription')

        # Deleting model 'DailyWakeupSubscription'
        db.delete_table(u'subscriptions_dailywakeupsubscription')

        # Deleting model 'DailyWakeupContent'
        db.delete_table(u'subscriptions_dailywakeupcontent')

        # Deleting model 'Vacation'
        db.delete_table(u'subscriptions_vacation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'subscriptions.dailywakeupcontent': {
            'Meta': {'object_name': 'DailyWakeupContent'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'daily_wakeup_subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subscriptions.DailyWakeupSubscription']"}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscription_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'subscription_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"})
        },
        u'subscriptions.dailywakeupsubscription': {
            'Meta': {'object_name': 'DailyWakeupSubscription', '_ormbases': [u'subscriptions.GenericSubscription']},
            u'genericsubscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['subscriptions.GenericSubscription']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'subscriptions.genericsubscription': {
            'Meta': {'object_name': 'GenericSubscription'},
            'appears_broken': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'avatar': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_borked_call_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_borked_calls': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pretty_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['subscriptions.Recipient']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'subscriptions.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'add_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dailywakeup_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'dailywakeup_hour': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'evening_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '12'}),
            'morning_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipients'", 'to': u"orm['auth.User']"}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sender_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'temperature': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {}),
            'wee_hours_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'subscriptions.tumblrsubscription': {
            'Meta': {'object_name': 'TumblrSubscription', '_ormbases': [u'subscriptions.GenericSubscription']},
            u'genericsubscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['subscriptions.GenericSubscription']", 'unique': 'True', 'primary_key': 'True'}),
            'last_post_ts': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'subscriptions.vacation': {
            'Meta': {'object_name': 'Vacation'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vacations'", 'to': u"orm['subscriptions.Recipient']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['subscriptions']