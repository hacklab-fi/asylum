# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0005_auto_20151128_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recurringtransaction',
            options={'verbose_name_plural': 'Recurring Transactions', 'verbose_name': 'Recurring Transaction'},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'verbose_name_plural': 'Transactions', 'verbose_name': 'Transaction'},
        ),
        migrations.AlterModelOptions(
            name='transactiontag',
            options={'verbose_name_plural': 'Transaction Tags', 'verbose_name': 'Transaction Tag'},
        ),
        migrations.AddField(
            model_name='recurringtransaction',
            name='end',
            field=models.DateField(db_index=True, blank=True, null=True, verbose_name='Until'),
        ),
        migrations.AddField(
            model_name='recurringtransaction',
            name='start',
            field=models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Since'),
        ),
    ]
