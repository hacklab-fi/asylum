# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import creditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0004_auto_20151128_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='unique_id',
            field=models.CharField(verbose_name='Unique transaction id', default=creditor.models.generate_transaction_id, unique=True, max_length=64),
        ),
    ]
