# Generated by Django 4.2 on 2023-10-02 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ratemanagement", "0002_ratepool_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="rateamounts",
            name="rate_rule_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ratemanagement.rateruletype",
                verbose_name="Rate Rule Type",
            ),
        ),
        migrations.AlterField(
            model_name="dayoftheweek",
            name="day_of_week",
            field=models.CharField(
                choices=[
                    ("Sun", "Sunday"),
                    ("Mon", "Monday"),
                    ("Tue", "Tuesday"),
                    ("Wed", "Wednesday"),
                    ("Thu", "Thursday"),
                    ("Fri", "Friday"),
                    ("Sat", "Saturday"),
                ],
                max_length=3,
                unique=True,
                verbose_name="Day of Week",
            ),
        ),
        migrations.AlterField(
            model_name="ratepool",
            name="code",
            field=models.CharField(
                max_length=10, unique=True, verbose_name="Rate Pool Code"
            ),
        ),
        migrations.AlterField(
            model_name="ratepool",
            name="name",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Rate Pool Name"
            ),
        ),
        migrations.AlterField(
            model_name="ratetype",
            name="rate_type",
            field=models.CharField(
                choices=[
                    ("System Generated", "System Generated"),
                    ("Weekend", "Weekend"),
                    ("Weekday", "Weekday"),
                    ("Seven Day", "Seven Day"),
                ],
                max_length=20,
                unique=True,
                verbose_name="Rate Type",
            ),
        ),
    ]
