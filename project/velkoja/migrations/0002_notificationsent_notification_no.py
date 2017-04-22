# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('velkoja', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationsent',
            name='notification_no',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
