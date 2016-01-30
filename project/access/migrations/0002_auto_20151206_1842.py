# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_markdown.models
from django.db import migrations, models

import asylum.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonMemberToken',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('label', models.CharField(max_length=200, verbose_name='Label', blank=True)),
                ('value', models.CharField(max_length=200, verbose_name='Token value')),
                ('revoked', models.BooleanField(verbose_name='Revoked', default=False)),
                ('contact', models.CharField(max_length=200, verbose_name='Contact')),
                ('notes', django_markdown.models.MarkdownField(verbose_name='Notes', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Non-member tokens',
                'verbose_name': 'Non-member token',
            },
            bases=(asylum.mixins.AtomicVersionMixin, asylum.mixins.CleanSaveMixin, models.Model),
        ),
        migrations.AlterModelOptions(
            name='accesstype',
            options={'verbose_name_plural': 'Access Types', 'verbose_name': 'Access Type'},
        ),
        migrations.AlterModelOptions(
            name='grant',
            options={'verbose_name_plural': 'Grants', 'verbose_name': 'Grant'},
        ),
        migrations.AlterModelOptions(
            name='token',
            options={'verbose_name_plural': 'Tokens', 'verbose_name': 'Token'},
        ),
        migrations.AlterModelOptions(
            name='tokentype',
            options={'verbose_name_plural': 'Token Types', 'verbose_name': 'Token Type'},
        ),
        migrations.AddField(
            model_name='grant',
            name='notes',
            field=django_markdown.models.MarkdownField(verbose_name='Notes', blank=True),
        ),
        migrations.AddField(
            model_name='nonmembertoken',
            name='grants',
            field=models.ManyToManyField(to='access.Grant', blank=True),
        ),
        migrations.AddField(
            model_name='nonmembertoken',
            name='ttype',
            field=models.ForeignKey(to='access.TokenType', related_name='+', verbose_name='Token type'),
        ),
    ]
