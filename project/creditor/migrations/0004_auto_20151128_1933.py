# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import creditor.models
from django.db import migrations, models


def generate_tids(apps, schema_editor):
    Transaction = apps.get_model('creditor', 'Transaction')
    for t in Transaction.objects.all().iterator():
        t.unique_id = creditor.models.generate_transaction_id()
        t.save()


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0003_auto_20151128_1923'),
    ]

    operations = [
        migrations.RunPython(
            generate_tids,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='unique_id',
            field=models.CharField(unique=True, verbose_name='Unique transaction id', max_length=32),
        ),
    ]
