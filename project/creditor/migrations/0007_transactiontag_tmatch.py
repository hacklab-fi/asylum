# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0006_auto_20151205_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiontag',
            name='tmatch',
            field=models.CharField(db_index=True, blank=True, verbose_name='Transaction match', max_length=20),
        ),
    ]
