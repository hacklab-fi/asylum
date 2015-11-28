# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('stamp', models.DateTimeField(auto_now_add=True, verbose_name='Datetime')),
                ('reference', models.CharField(verbose_name='Reference', max_length=200)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Amount')),
                ('owner', models.ForeignKey(to='members.Member', verbose_name='Member', related_name='creditor_transactions')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionTag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Label', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='tag',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Tag', to='creditor.TransactionTag'),
        ),
    ]
