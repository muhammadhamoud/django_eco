# Generated by Django 4.2 on 2023-11-03 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_attribute_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TagTranslation',
        ),
    ]