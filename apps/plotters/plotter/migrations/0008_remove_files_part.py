# Generated by Django 4.2 on 2024-01-20 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plotter', '0007_bodypart_alter_files_application_alter_files_part_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='part',
        ),
    ]