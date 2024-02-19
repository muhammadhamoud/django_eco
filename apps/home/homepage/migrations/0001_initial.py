# Generated by Django 4.2 on 2023-10-23 07:03

import core.models
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SiteInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SiteInformationAdditional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siteinformationadditional', to='homepage.siteinformation')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teammembers', to='homepage.siteinformation')),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='homepage.siteinformation')),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SiteMetaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='home/')),
                ('address', models.TextField(blank=True, null=True)),
                ('telephone', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('sales_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('technical_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('accounts_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('whatsapp_url', models.URLField(blank=True, null=True)),
                ('googlemap_url', models.URLField(blank=True, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sitemetadata', to='homepage.siteinformation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='homepage.siteinformation')),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
                ('client', models.CharField(max_length=256)),
                ('file', models.FileField(upload_to='')),
                ('is_published', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.businesscategory')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='homepage.siteinformation')),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.businesscategory')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='homepage.siteinformation')),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketings', to='homepage.siteinformation')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload an image for the content.', null=True, upload_to=core.models.base_image_path, validators=[core.models.validate_image_extension], verbose_name='Image')),
                ('icon', models.CharField(blank=True, help_text='Enter an icon for the content.', max_length=100, null=True, verbose_name='Icon')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time when the content was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='The date and time when the content was last modified.', verbose_name='Modified')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='homepage.siteinformation')),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='businesscategory',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_categories', to='homepage.siteinformation'),
        ),
        migrations.CreateModel(
            name='TestimonialTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.testimonial')),
            ],
            options={
                'verbose_name': 'testimonial Translation',
                'db_table': 'homepage_testimonial_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TeamMemberTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.teammember')),
            ],
            options={
                'verbose_name': 'team member Translation',
                'db_table': 'homepage_teammember_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SiteInformationTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('site_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('site_description', models.TextField(blank=True, null=True)),
                ('site_keywords', models.CharField(blank=True, max_length=200, null=True)),
                ('tagline', models.CharField(blank=True, max_length=256, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.siteinformation')),
            ],
            options={
                'verbose_name': 'site information Translation',
                'db_table': 'homepage_siteinformation_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SiteInformationAdditionalTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('about_us', models.TextField(blank=True, null=True)),
                ('privacy_policy', models.TextField(blank=True, null=True)),
                ('terms_of_service', models.TextField(blank=True, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.siteinformationadditional')),
            ],
            options={
                'verbose_name': 'site information additional Translation',
                'db_table': 'homepage_siteinformationadditional_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ServiceTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.service')),
            ],
            options={
                'verbose_name': 'service Translation',
                'db_table': 'homepage_service_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.project')),
            ],
            options={
                'verbose_name': 'project Translation',
                'db_table': 'homepage_project_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OfferingTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.offering')),
            ],
            options={
                'verbose_name': 'offering Translation',
                'db_table': 'homepage_offering_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MarketingTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.marketing')),
            ],
            options={
                'verbose_name': 'marketing Translation',
                'db_table': 'homepage_marketing_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FeatureTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.feature')),
            ],
            options={
                'verbose_name': 'feature Translation',
                'db_table': 'homepage_feature_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BusinessCategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a name for the content.', max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Enter a slug for the content.', null=True, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, help_text='Enter a description for the content.', null=True, verbose_name='Description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='homepage.businesscategory')),
            ],
            options={
                'verbose_name': 'business category Translation',
                'db_table': 'homepage_businesscategory_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
