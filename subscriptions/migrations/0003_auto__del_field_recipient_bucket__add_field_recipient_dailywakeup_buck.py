# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Recipient.bucket'
        db.delete_column(u'subscriptions_recipient', 'bucket')

        # Adding field 'Recipient.dailywakeup_bucket'
        db.add_column(u'subscriptions_recipient', 'dailywakeup_bucket',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Recipient.localnoon_bucket'
        db.add_column(u'subscriptions_recipient', 'localnoon_bucket',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Recipient.morning_bucket'
        db.add_column(u'subscriptions_recipient', 'morning_bucket',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Recipient.evening_bucket'
        db.add_column(u'subscriptions_recipient', 'evening_bucket',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Recipient.wee_hours_bucket'
        db.add_column(u'subscriptions_recipient', 'wee_hours_bucket',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Recipient.bucket'
        db.add_column(u'subscriptions_recipient', 'bucket',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Deleting field 'Recipient.dailywakeup_bucket'
        db.delete_column(u'subscriptions_recipient', 'dailywakeup_bucket')

        # Deleting field 'Recipient.localnoon_bucket'
        db.delete_column(u'subscriptions_recipient', 'localnoon_bucket')

        # Deleting field 'Recipient.morning_bucket'
        db.delete_column(u'subscriptions_recipient', 'morning_bucket')

        # Deleting field 'Recipient.evening_bucket'
        db.delete_column(u'subscriptions_recipient', 'evening_bucket')

        # Deleting field 'Recipient.wee_hours_bucket'
        db.delete_column(u'subscriptions_recipient', 'wee_hours_bucket')


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
            'delivery_bucket': ('django.db.models.fields.IntegerField', [], {}),
            'delivery_time': ('django.db.models.fields.IntegerField', [], {}),
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
        u'subscriptions.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            's2g_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'s2g_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'subscriptions.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'add_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dailywakeup_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'evening_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localnoon_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'morning_bucket': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipients'", 'to': u"orm['auth.User']"}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sender_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'default': "'America/Los_Angeles'"}),
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