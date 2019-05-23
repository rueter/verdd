# Generated by Django 2.2.1 on 2019-05-23 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageXML', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=250)),
                ('added_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AddField(
            model_name='element',
            name='imported_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manageXML.DataFile'),
        ),
    ]