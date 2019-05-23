# Generated by Django 2.2.1 on 2019-05-23 17:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manageXML', '0003_auto_20190523_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datafile',
            old_name='language',
            new_name='lang_source',
        ),
        migrations.AddField(
            model_name='datafile',
            name='lang_target',
            field=models.CharField(default='sms', max_length=3),
            preserve_default=False,
        ),
    ]
