# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170805_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternetRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exists', models.BooleanField(default=False, verbose_name='Exists')),
                ('speed', models.IntegerField(blank=True, choices=[(1, 'Less than 1 Mbps'), (3, 'Between 1 and 3 Mbps'), (5, 'Between 3 and 5 Mbps'), (10, 'Between 5 and 10 Mbps'), (20, 'Between 10 and 20 Mbps'), (50, 'Between 20 and 50 Mbps'), (100, 'Between 50 and 100 Mbps'), (1000, 'More than 100 Mbps')], null=True)),
                ('is_open', models.BooleanField(default=False, verbose_name='Is Open')),
                ('password', models.CharField(max_length=200, verbose_name='Password')),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='drink',
            field=models.TextField(default='N/A', verbose_name='Drink'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rating',
            name='food',
            field=models.TextField(verbose_name='Food'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='internet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.InternetRating'),
        ),
    ]
