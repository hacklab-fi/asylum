# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import asylum.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipApplicationTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Label', max_length=200)),
            ],
            bases=(asylum.mixins.AtomicVersionMixin, models.Model),
        ),
        migrations.AddField(
            model_name='membershipapplication',
            name='tags',
            field=models.ManyToManyField(verbose_name='Application tags', blank=True, to='members.MembershipApplicationTag', related_name='_tags_+'),
        ),
    ]
