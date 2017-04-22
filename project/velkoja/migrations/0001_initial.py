# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models

import asylum.mixins


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationSent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('stamp', models.DateTimeField(db_index=True, verbose_name='Datetime', default=django.utils.timezone.now)),
                ('transaction_unique_id', models.CharField(verbose_name='Unique transaction id', max_length=64, unique=True)),
                ('email', models.EmailField(verbose_name='Email address', max_length=254)),
            ],
            options={
                'abstract': False,
            },
            bases=(asylum.mixins.AtomicVersionMixin, asylum.mixins.CleanSaveMixin, models.Model),
        ),
    ]
