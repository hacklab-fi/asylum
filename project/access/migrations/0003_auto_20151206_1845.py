# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_auto_20151206_1842'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='grant',
            unique_together=set([('owner', 'atype')]),
        ),
    ]
