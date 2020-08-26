# Generated by Django 2.2.1 on 2020-06-16 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import manageXML.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manageXML', '0017_historicallexememetadata_lexememetadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrelationmetadata',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, 'Generic'), (1, 'Specification')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='relationmetadata',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, 'Generic'), (1, 'Specification')], default=None, null=True),
        ),
        migrations.CreateModel(
            name='HistoricalStem',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('text', manageXML.fields.BinaryCharField(max_length=250)),
                ('contlex', models.CharField(blank=True, max_length=250)),
                ('notes', models.CharField(blank=True, max_length=250)),
                ('order', models.IntegerField(default=0)),
                ('checked', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(blank=True, editable=False, verbose_name='date published')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('lexeme', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='manageXML.Lexeme')),
            ],
            options={
                'verbose_name': 'historical stem',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Stem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', manageXML.fields.BinaryCharField(max_length=250)),
                ('contlex', models.CharField(blank=True, max_length=250)),
                ('notes', models.CharField(blank=True, max_length=250)),
                ('order', models.IntegerField(default=0)),
                ('checked', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stems', to=settings.AUTH_USER_MODEL)),
                ('lexeme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manageXML.Lexeme')),
            ],
            options={
                'unique_together': {('lexeme', 'text')},
            },
        ),
    ]
