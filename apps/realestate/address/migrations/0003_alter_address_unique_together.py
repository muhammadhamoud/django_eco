# Generated by Django 4.2 on 2023-11-23 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_alter_address_primary_alter_address_type_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set(),
        ),
    ]
