# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_markdown.models
from django.db import migrations, models

import asylum.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20151128_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('stamp', models.DateTimeField(verbose_name='Datetime', auto_now_add=True, db_index=True)),
                ('notes', django_markdown.models.MarkdownField(verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
                'ordering': ['-stamp'],
            },
            bases=(asylum.mixins.AtomicVersionMixin, asylum.mixins.CleanSaveMixin, models.Model),
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['lname', 'fname']},
        ),
        migrations.AlterModelOptions(
            name='membershipapplication',
            options={'verbose_name': 'Membership Application', 'verbose_name_plural': 'Membership Applications'},
        ),
        migrations.AlterModelOptions(
            name='membershipapplicationtag',
            options={'verbose_name': 'Membership Application Tag', 'verbose_name_plural': 'Membership Application Tags'},
        ),
        migrations.AlterModelOptions(
            name='membertype',
            options={'verbose_name': 'Member Type', 'verbose_name_plural': 'Member Types'},
        ),
        migrations.AddField(
            model_name='membershipapplication',
            name='notes',
            field=django_markdown.models.MarkdownField(verbose_name='Notes', blank=True),
        ),
        migrations.AddField(
            model_name='membernote',
            name='member',
            field=models.ForeignKey(verbose_name='Member', blank=True, null=True, to='members.Member', related_name='notes'),
        ),
    ]
