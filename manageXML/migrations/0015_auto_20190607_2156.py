# Generated by Django 2.2.1 on 2019-06-07 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageXML', '0014_remove_affiliation_pageid'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='assonance',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='element',
            name='assonance_rev',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='element',
            name='consonance',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='element',
            name='consonance_rev',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalelement',
            name='assonance',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalelement',
            name='assonance_rev',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalelement',
            name='consonance',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalelement',
            name='consonance_rev',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
