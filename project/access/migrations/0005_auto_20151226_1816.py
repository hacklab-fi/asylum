# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_auto_20151211_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonmembertoken',
            name='grants',
            field=models.ManyToManyField(verbose_name='Access', to='access.AccessType', blank=True, related_name='_grants_+'),
        ),
        migrations.AlterUniqueTogether(
            name='nonmembertoken',
            unique_together=set([('ttype', 'value')]),
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set([('ttype', 'value')]),
        ),
    ]
