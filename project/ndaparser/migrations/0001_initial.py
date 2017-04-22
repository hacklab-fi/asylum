# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import asylum.mixins
import ndaparser.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('file', models.FileField(upload_to=ndaparser.models.datestamped_and_normalized)),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('last_transaction', models.DateField()),
                ('user', models.ForeignKey(on_delete=models.SET(ndaparser.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Uploaded transaction',
                'verbose_name_plural': 'Uploaded transaction',
                'ordering': ['-stamp'],
            },
            bases=(asylum.mixins.AtomicVersionMixin, asylum.mixins.CleanSaveMixin, models.Model),
        ),
    ]
