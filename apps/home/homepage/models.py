from django.db import models
from core.models import Extensions
from django.urls import reverse
from core.models import base_image_path, validate_image_extension
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.db import models
from django.utils.translation import gettext as _
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

from core.models import BaseContent, DRY_TRANSLATION

	
class SiteInformation(Extensions, TranslatableModel):
	# Site Information Fields
	translations = DRY_TRANSLATION
	company_name = models.CharField(max_length=100, blank=True, null=True)
	keywords = models.CharField(max_length=200, blank=True, null=True)
	license_number = models.CharField(max_length=200, blank=True, null=True)
	vat_number = models.CharField(max_length=200, blank=True, null=True)
	register_number = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return str(self.name)
	
	def save(self, *args, **kwargs):
		# self.name = str(self.name).title()
		super(SiteInformation, self).save(*args, **kwargs)

class SiteMetaData(Extensions):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='sitemetadata')
	logo = models.ImageField(
		upload_to='home/',
		validators=[validate_image_extension],
		blank=True,
		null=True,
		help_text=_("Upload Logo image."),
		verbose_name=_("Logo Image")
	)
	icon = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		help_text=_("Enter an icon for the content."),
		verbose_name=_("Icon")
	)
	# Contact Information Fields
	address = models.TextField(blank=True, null=True)
	telephone = models.CharField(blank=True, null=True, max_length=20)
	mobile = models.CharField(blank=True, null=True, max_length=20)
	fax = models.CharField(blank=True, null=True, max_length=20)
	email = models.EmailField(blank=True, null=True)
	website = models.URLField(blank=True, null=True)
	sales_email = models.EmailField(blank=True, null=True)
	technical_email = models.EmailField(blank=True, null=True)
	accounts_email = models.EmailField(blank=True, null=True)

	# Social Media URLs
	facebook_url = models.URLField(blank=True, null=True)
	twitter_url = models.URLField(blank=True, null=True)
	instagram_url = models.URLField(blank=True, null=True)
	linkedin_url = models.URLField(blank=True, null=True)
	whatsapp_url = models.URLField(blank=True, null=True)
	googlemap_url = models.URLField(blank=True, null=True)

	def __str__(self):
		return str(self.site.name)

class SiteInformationAdditional(Extensions, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='siteinformationadditional')
	# Additional Site Information Fields
	translations = TranslatedFields(
		about_us = models.TextField(blank=True, null=True),
		privacy_policy = models.TextField(blank=True, null=True),
		terms_of_service = models.TextField(blank=True, null=True),
		tagline = models.CharField(max_length=200, blank=True, null=True),
	)
	
	def __str__(self):
		return str(self.site.name)




class Marketing(TranslatableModel, BaseContent):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='marketings')
	translations = DRY_TRANSLATION
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('marketing-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		self.slug = slugify(self.name)
		super(Marketing, self).save(*args, **kwargs)
	
class Service(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='services')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('service-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		self.slug = slugify(self.name)
		super(Service, self).save(*args, **kwargs)

class Feature(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='features')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('feature-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		# self.slug = slugify(self.name)
		super(Feature, self).save(*args, **kwargs)

class BusinessCategory(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='product_categories')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('product-category-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		self.slug = slugify(self.name)
		super(BusinessCategory, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Business Categories'
    
class Offering(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='products')
	translations = DRY_TRANSLATION
	category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('product-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		self.slug = slugify(self.name)
		super(Offering, self).save(*args, **kwargs)

class Project(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='projects')
	translations = DRY_TRANSLATION
	category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
	client = models.CharField(max_length=256, blank=True, null=True)
	file = models.FileField(blank=True, null=True)
	is_published = models.BooleanField(default=False)

	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('project-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		self.slug = slugify(self.name)
		super(Project, self).save(*args, **kwargs)

class TeamMember(BaseContent, TranslatableModel):
	# Personal Information
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='teammembers')
	
	translations = TranslatedFields(
		name=models.CharField(
			max_length=100,
			help_text=_("Enter a name for the content."),
			verbose_name=_("Name"),
			blank=True,
			null=True	
		),
		description=models.TextField(
			blank=True,
			null=True,
			help_text=_("Enter a description for the content."),
			verbose_name=_("Description")
		),
		job_title = models.CharField(max_length=100, blank=True, null=True),
		bio = models.TextField(blank=True, null=True),
	)
	
	email = models.EmailField(blank=True, null=True)
	phone_number = models.CharField(max_length=20, blank=True, null=True)
	location = models.CharField(max_length=256, blank=True, null=True)

	# Social Media Profiles (optional)
	whatsapp = models.URLField(blank=True, null=True)
	linkedin = models.URLField(blank=True, null=True)
	twitter = models.URLField(blank=True, null=True)
	facebook = models.URLField(blank=True, null=True)
	instagram = models.URLField(blank=True, null=True)
	github = models.URLField(blank=True, null=True)
	medium = models.URLField(blank=True, null=True)

	def __str__(self):
		return f"{str(self.name)} - {self.job_title}"
	
	def get_absolute_url(self):
		return reverse('teammember-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		# self.slug = slugify(self.name)
		super(TeamMember, self).save(*args, **kwargs)
	
class Testimonial(BaseContent, TranslatableModel):
	translations = TranslatedFields(
		name=models.CharField(
			max_length=100,
			help_text=_("Enter a name for the content."),
			verbose_name=_("Name"),
			blank=True,
			null=True	
		),
		description=models.TextField(
			blank=True,
			null=True,
			help_text=_("Enter a description for the content."),
			verbose_name=_("Description")
		),
		job_title = models.CharField(max_length=100, blank=True, null=True),
		company = models.CharField(max_length=100, blank=True, null=True),
		content = models.TextField(blank=True, null=True),
	)
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='testimonials')
	
	def __str__(self):
		return f"{str(self.name)} - {self.company}"
	
	def get_absolute_url(self):
		return reverse('testimonial-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.name = str(self.name).title()
		self.slug = slugify(self.name)
		super(Testimonial, self).save(*args, **kwargs)



"""
Front-End Developer
Back-End Developer
Full-Stack Developer
Web Developer
UI/UX Designer
Web Application Developer
E-commerce Developer
Mobile App Developer
CMS Developer
Web Security Specialist
Web Accessibility Specialist
DevOps Engineer
Web Project Manager
Web Content Writer/Copywriter
Web Quality Assurance (QA) Tester

Data Scientist
Machine Learning Engineer
Data Analyst
Business Analyst
Data Engineer
Statistical Analyst
Quantitative Analyst (Quant)
Data Science Manager
Machine Learning Researcher
Data Science Consultant
Data Visualization Specialist
Natural Language Processing (NLP) Engineer
Computer Vision Engineer
AI Ethicist
Predictive Modeler
Healthcare Data Analyst

"""