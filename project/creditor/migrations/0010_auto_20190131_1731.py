# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditor', '0009_auto_20160123_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringtransaction',
            name='rtype',
            field=models.PositiveSmallIntegerField(verbose_name='Recurrence type', choices=[(1, 'Monthly'), (2, 'Yearly'), (3, 'Quarterly')]),
        ),
    ]
