# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_auto_20151206_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonmembertoken',
            name='grants',
            field=models.ManyToManyField(to='access.AccessType', blank=True, related_name='_grants_+'),
        ),
    ]
