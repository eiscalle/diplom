# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'user_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'user', ['Tag'])

        # Adding model 'PortalUser'
        db.create_table(u'user_portaluser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=256, db_index=True)),
            ('personal_email', self.gf('django.db.models.fields.EmailField')(max_length=256, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=256, null=True, blank=True)),
            ('leader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.PortalUser'], null=True, blank=True)),
            ('mobile_phone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('work_phone', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('placement_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_fabric', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'user', ['PortalUser'])

        # Adding M2M table for field groups on 'PortalUser'
        m2m_table_name = db.shorten_name(u'user_portaluser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('portaluser', models.ForeignKey(orm[u'user.portaluser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['portaluser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'PortalUser'
        m2m_table_name = db.shorten_name(u'user_portaluser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('portaluser', models.ForeignKey(orm[u'user.portaluser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['portaluser_id', 'permission_id'])

        # Adding M2M table for field tag on 'PortalUser'
        m2m_table_name = db.shorten_name(u'user_portaluser_tag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('portaluser', models.ForeignKey(orm[u'user.portaluser'], null=False)),
            ('tag', models.ForeignKey(orm[u'user.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['portaluser_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'user_tag')

        # Deleting model 'PortalUser'
        db.delete_table(u'user_portaluser')

        # Removing M2M table for field groups on 'PortalUser'
        db.delete_table(db.shorten_name(u'user_portaluser_groups'))

        # Removing M2M table for field user_permissions on 'PortalUser'
        db.delete_table(db.shorten_name(u'user_portaluser_user_permissions'))

        # Removing M2M table for field tag on 'PortalUser'
        db.delete_table(db.shorten_name(u'user_portaluser_tag'))


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'user.portaluser': {
            'Meta': {'object_name': 'PortalUser'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fabric': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.PortalUser']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'personal_email': ('django.db.models.fields.EmailField', [], {'max_length': '256', 'blank': 'True'}),
            'placement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'tag_user'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['user.Tag']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'work_email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'})
        },
        u'user.tag': {
            'Meta': {'object_name': 'Tag'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['user']