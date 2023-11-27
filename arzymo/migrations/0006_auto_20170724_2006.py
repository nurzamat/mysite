# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arzymo', '0005_cafe'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='arzymo.Post')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price_currency', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DatingPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='arzymo.Post')),
                ('sex', models.BooleanField(default=0)),
                ('birth_year', models.DateField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cafe',
            name='place_ptr',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='place_ptr',
        ),
        migrations.RemoveField(
            model_name='post',
            name='birth_year',
        ),
        migrations.RemoveField(
            model_name='post',
            name='price',
        ),
        migrations.RemoveField(
            model_name='post',
            name='price_currency',
        ),
        migrations.RemoveField(
            model_name='post',
            name='sex',
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Cafe',
        ),
        migrations.DeleteModel(
            name='Place',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]
