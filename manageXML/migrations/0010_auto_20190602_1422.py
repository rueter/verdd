# Generated by Django 2.2.1 on 2019-06-02 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageXML', '0009_auto_20190601_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsource',
            name='element',
        ),
        migrations.RemoveField(
            model_name='source',
            name='element',
        ),
        migrations.AddField(
            model_name='historicalsource',
            name='translation',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='manageXML.Translation'),
        ),
        migrations.AddField(
            model_name='source',
            name='translation',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='manageXML.Translation'),
            preserve_default=False,
        ),
    ]
