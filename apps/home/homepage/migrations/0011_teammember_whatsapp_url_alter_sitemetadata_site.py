# Generated by Django 4.2 on 2023-10-30 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_alter_sitemetadata_logo_alter_sitemetadata_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='whatsapp_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sitemetadata',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sitemetadata', to='homepage.siteinformation'),
        ),
    ]
