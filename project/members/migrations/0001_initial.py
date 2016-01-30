# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import members.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('fname', models.CharField(verbose_name='First name', max_length=200)),
                ('lname', models.CharField(verbose_name='Last name', max_length=200)),
                ('city', models.CharField(verbose_name='City of residence', max_length=200)),
                ('email', models.EmailField(verbose_name='Email address', unique=True, max_length=254)),
                ('phone', models.CharField(verbose_name='Phone number', blank=True, max_length=200)),
                ('nick', models.CharField(verbose_name='Nickname', blank=True, max_length=200)),
                ('accepted', models.DateField(auto_now_add=True, verbose_name='Date accepted')),
                ('anonymized_id', models.CharField(verbose_name='Anonymized id (for use in external databases)', default=members.models.generate_unique_randomid, null=True, unique=True, blank=True, max_length=24)),
                ('member_id', models.PositiveIntegerField(default=members.models.generate_unique_memberid, verbose_name='Member id no', blank=True, unique=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembershipApplication',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('fname', models.CharField(verbose_name='First name', max_length=200)),
                ('lname', models.CharField(verbose_name='Last name', max_length=200)),
                ('city', models.CharField(verbose_name='City of residence', max_length=200)),
                ('email', models.EmailField(verbose_name='Email address', unique=True, max_length=254)),
                ('phone', models.CharField(verbose_name='Phone number', blank=True, max_length=200)),
                ('nick', models.CharField(verbose_name='Nickname', blank=True, max_length=200)),
                ('received', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('label', models.CharField(verbose_name='Label', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='mtypes',
            field=models.ManyToManyField(related_name='_mtypes_+', to='members.MemberType', verbose_name='Membership types', blank=True),
        ),
    ]
