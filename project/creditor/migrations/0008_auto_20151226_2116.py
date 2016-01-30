# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0007_transactiontag_tmatch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='stamp',
            field=models.DateTimeField(verbose_name='Datetime', default=django.utils.timezone.now, db_index=True),
        ),
    ]
