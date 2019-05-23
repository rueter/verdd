# Generated by Django 2.2.1 on 2019-05-23 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageXML', '0002_auto_20190523_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='element',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='etymon',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='source',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='stem',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
    ]