# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0008_auto_20151226_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recurringtransaction',
            options={'ordering': ['owner__lname', 'owner__fname', '-start'], 'verbose_name': 'Recurring Transaction', 'verbose_name_plural': 'Recurring Transactions'},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-stamp', 'reference'], 'verbose_name': 'Transaction', 'verbose_name_plural': 'Transactions'},
        ),
        migrations.AlterModelOptions(
            name='transactiontag',
            options={'ordering': ['label'], 'verbose_name': 'Transaction Tag', 'verbose_name_plural': 'Transaction Tags'},
        ),
        migrations.AddField(
            model_name='transactiontag',
            name='holvi_code',
            field=models.CharField(blank=True, verbose_name='Holvi category code', db_index=True, max_length=64),
        ),
    ]
