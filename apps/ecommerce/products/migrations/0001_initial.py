# Generated by Django 4.2 on 2023-10-11 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import products.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the category.', max_length=200, unique=True, verbose_name='Name')),
                ('icon', models.ImageField(blank=True, upload_to=products.models.category_image_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image', models.ImageField(blank=True, upload_to=products.models.product_image_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('views', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='products.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_product', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ip', models.CharField(max_length=250)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_views', to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
