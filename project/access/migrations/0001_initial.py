# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('label', models.CharField(verbose_name='Label', max_length=200)),
                ('bit', models.PositiveSmallIntegerField(null=True, verbose_name='Bit number', unique=True, blank=True)),
                ('external_id', models.CharField(null=True, blank=True, verbose_name='External identifier', unique=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('atype', models.ForeignKey(to='access.AccessType', verbose_name='Access', related_name='+')),
                ('owner', models.ForeignKey(to='members.Member', verbose_name='Member', related_name='access_granted')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('label', models.CharField(blank=True, verbose_name='Label', max_length=200)),
                ('value', models.CharField(verbose_name='Token value', max_length=200)),
                ('revoked', models.BooleanField(default=False, verbose_name='Revoked')),
                ('owner', models.ForeignKey(to='members.Member', verbose_name='Member', related_name='access_tokens')),
            ],
        ),
        migrations.CreateModel(
            name='TokenType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('label', models.CharField(verbose_name='Label', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='ttype',
            field=models.ForeignKey(to='access.TokenType', verbose_name='Token type', related_name='+'),
        ),
    ]
