# Generated by Django 5.0.1 on 2024-02-18 19:50

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse", "0002_remove_category_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="categorytranslation",
            name="slug",
        ),
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.CharField(
                blank=True,
                help_text="Enter an icon for the content.",
                max_length=100,
                null=True,
                verbose_name="Icon",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Upload an image for the content.",
                null=True,
                upload_to=core.models.base_image_path,
                validators=[core.models.validate_image_extension],
                verbose_name="Image",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Enter a slug for the content.",
                null=True,
                unique=True,
                verbose_name="Slug",
            ),
        ),
    ]
