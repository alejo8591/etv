# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('users_userprofile', (
            ('identification', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('refFranchisee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'], null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('dateOfBirth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('alternativePhone', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('lastAccess', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('activationKey', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('keyExpires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('refFranchiseeCode', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('users', ['UserProfile'])

        # Adding model 'CreateCodes'
        db.create_table('users_createcodes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('franchisee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('useFlagCode', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dateUseFlag', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dateCreateCode', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('users', ['CreateCodes'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('users_userprofile')

        # Deleting model 'CreateCodes'
        db.delete_table('users_createcodes')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.createcodes': {
            'Meta': {'object_name': 'CreateCodes'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'dateCreateCode': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateUseFlag': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'franchisee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'useFlagCode': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'users.userprofile': {
            'Meta': {'ordering': "['identification']", 'object_name': 'UserProfile'},
            'activationKey': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'alternativePhone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'dateOfBirth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'identification': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'keyExpires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lastAccess': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'refFranchisee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'refFranchiseeCode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['users']