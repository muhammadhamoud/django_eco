# Generated by Django 4.2 on 2023-11-23 19:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
    ]