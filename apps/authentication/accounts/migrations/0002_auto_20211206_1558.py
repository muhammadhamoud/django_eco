# Generated by Django 3.0 on 2021-12-06 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='provider',
            new_name='auth_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='social_id',
        ),
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(default='email', max_length=255),
        ),
    ]
