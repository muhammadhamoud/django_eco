# Generated by Django 4.2 on 2023-10-30 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_rename_facebook_url_teammember_facebook_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teammember',
            name='medium',
            field=models.URLField(blank=True, null=True),
        ),
    ]
