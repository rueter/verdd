# Generated by Django 2.2.1 on 2020-06-02 00:33

from django.db import migrations
import manageXML.fields


class Migration(migrations.Migration):

    dependencies = [
        ('manageXML', '0014_auto_20200517_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicallexeme',
            name='lexeme',
            field=manageXML.fields.BinaryCharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='lexeme',
            name='lexeme',
            field=manageXML.fields.BinaryCharField(max_length=250),
        ),
    ]
