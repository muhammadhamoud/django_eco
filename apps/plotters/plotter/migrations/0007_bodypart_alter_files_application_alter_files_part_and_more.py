# Generated by Django 4.2 on 2024-01-20 09:04

import core.models
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('plotter', '0006_alter_files_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
            ],
            options={
                'verbose_name': 'Body Part',
                'verbose_name_plural': 'Body Parts',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='files',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_files', to='plotter.application'),
        ),
        migrations.AlterField(
            model_name='files',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='body_part_files', to='plotter.bodypart'),
        ),
        migrations.CreateModel(
            name='BodyPartTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(blank=True, help_text='Enter a name for the content.', max_length=100, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='plotter.bodypart')),
            ],
            options={
                'verbose_name': 'Body Part Translation',
                'db_table': 'plotter_bodypart_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
