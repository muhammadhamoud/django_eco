# Generated by Django 4.2 on 2024-01-23 19:55

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('plotter', '0014_delete_cartranslation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(blank=True, help_text='Enter a name for the content.', max_length=100, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='plotter.car')),
            ],
            options={
                'verbose_name': 'Car Translation',
                'db_table': 'plotter_car_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
