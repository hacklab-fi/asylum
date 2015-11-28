# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('creditor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringTransaction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('label', models.CharField(max_length=200, blank=True, verbose_name='Label')),
                ('rtype', models.PositiveSmallIntegerField(choices=[(1, 'Monthly'), (2, 'Yearly')], verbose_name='Recurrence type')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Amount')),
                ('owner', models.ForeignKey(related_name='+', to='members.Member', verbose_name='Member')),
                ('tag', models.ForeignKey(related_name='+', to='creditor.TransactionTag', verbose_name='Tag')),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tag',
            field=models.ForeignKey(null=True, related_name='+', blank=True, to='creditor.TransactionTag', verbose_name='Tag'),
        ),
    ]
