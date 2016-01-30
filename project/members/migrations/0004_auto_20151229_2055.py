# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20151206_1908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': 'Member', 'verbose_name_plural': 'Members'},
        ),
        migrations.AlterModelOptions(
            name='membernote',
            options={'verbose_name': 'Note', 'ordering': ['member__lname', 'member__fname', '-stamp'], 'verbose_name_plural': 'Notes'},
        ),
        migrations.AlterField(
            model_name='member',
            name='accepted',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date accepted'),
        ),
        migrations.AlterField(
            model_name='membernote',
            name='stamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Datetime', db_index=True),
        ),
        migrations.AlterField(
            model_name='membershipapplication',
            name='received',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
