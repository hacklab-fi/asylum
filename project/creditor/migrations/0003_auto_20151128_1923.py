# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0002_auto_20151128_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='unique_id',
            field=models.CharField(blank=True, null=True, max_length=32, verbose_name='Unique transaction id'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reference',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Reference'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='stamp',
            field=models.DateTimeField(db_index=True, verbose_name='Datetime', auto_now_add=True),
        ),
    ]
