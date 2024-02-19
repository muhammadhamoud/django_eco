# Generated by Django 4.2 on 2023-10-22 11:54

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute',
            options={'ordering': ['-modified', 'name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-modified', 'name']},
        ),
        migrations.AlterModelOptions(
            name='productlabel',
            options={'ordering': ['-modified', 'name']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-modified', 'name']},
        ),
        migrations.AddField(
            model_name='attribute',
            name='icon',
            field=models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='slug',
            field=models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='product',
            name='icon',
            field=models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='productlabel',
            name='icon',
            field=models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon'),
        ),
        migrations.AddField(
            model_name='productlabel',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='productlabel',
            name='slug',
            field=models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='tag',
            name='icon',
            field=models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon'),
        ),
        migrations.AddField(
            model_name='tag',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='modified',
            field=models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='modified',
            field=models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='productlabel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='productlabel',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productlabel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='productlabel',
            name='modified',
            field=models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='productlabel',
            name='name',
            field=models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='modified',
            field=models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name'),
        ),
    ]
