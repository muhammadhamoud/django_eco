# Generated by Django 4.2 on 2023-10-16 16:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_profile_one_click_purchasing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]