from django.db import models
from django.db import models
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify
from core.models import (
    Extensions,
    BaseContent,
    DRY_TRANSLATION,
    base_file_path_protected,
)
from core.models import base_image_path, validate_image_extension

END_DATE = settings.END_DATE

class Year(models.Model):
    year = models.PositiveIntegerField(unique=True, help_text=_("Enter the year"))

    def __str__(self):
        return str(self.year)

class Application(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("portter:application", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Update the slug using the name field
        # self.name = str(self.name).title()
        self.slug = slugify(self.name)
        super(Application, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")
        # ordering = [f'translations__name']

class Body(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("portter:Body", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Update the slug using the name field
        # self.name = str(self.name).title()
        self.slug = slugify(self.name)
        super(Body, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Body")
        verbose_name_plural = _("Bodies")
        # ordering = [f'translations__name']

class BodyPart(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="application_body_parts"
    )
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("portter:body_part", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Update the slug using the name field
        # self.name = str(self.name).title()
        self.slug = slugify(self.name)
        super(BodyPart, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Body Part")
        verbose_name_plural = _("Body Parts")

class Width(models.Model):
    width = models.PositiveIntegerField(unique=True, help_text=_("Enter the width"))

    def __str__(self):
        return str(self.width)

class Height(models.Model):
    height = models.PositiveIntegerField(unique=True, help_text=_("Enter the height"))

    def __str__(self):
        return str(self.height)

class PlotterMachine(BaseContent):
    name = models.CharField(
        max_length=100,
        help_text=_("Enter a name for the content."),
        verbose_name=_("Name"),
        blank=True,
        null=True,
        unique=True,
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("portter:plotter", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Update the slug using the name field
        # self.name = str(self.name).title()
        self.slug = slugify(self.name)
        super(PlotterMachine, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Plotter Machine")
        verbose_name_plural = _("Plotter Machines")

class Make(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("portter:make", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Update the slug using the name field
        # self.name = str(self.name).title()
        self.slug = slugify(self.name)
        super(Make, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Make")
        verbose_name_plural = _("Makes")
        # ordering = [f'translations__name']

class Model(TranslatableModel, BaseContent):
    make = models.ForeignKey(
        Make, on_delete=models.CASCADE, null=True, related_name="makes"
    )
    translations = DRY_TRANSLATION

    def __str__(self):
        return f"{str(self.make.name)} {str(self.name)}"

    def get_absolute_url(self):
        return reverse("portter:model", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Update the slug using the name field
        # self.name = str(self.name).title()
        self.slug = slugify(f"{str(self.make.name)} {str(self.name)}")
        super(Model, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Model")
        verbose_name_plural = _("Models")
        # ordering = [f'translations__name']

class Trim(TranslatableModel, BaseContent):
    model = models.ForeignKey(
        Model, on_delete=models.CASCADE, null=True, related_name="models"
    )
    translations = DRY_TRANSLATION

    def __str__(self):
        return f"{str(self.model.make.name)} {str(self.model.name)} {str(self.name)}"

    def get_absolute_url(self):
        return reverse("portter:trim", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Update the slug using the name field
        # self.name = str(self.name).title()
        self.slug = slugify(f"{str(self.model.make.name)} {str(self.model.name)} {str(self.name)}")
        super(Trim, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Trim")
        verbose_name_plural = _("Trims")
        # ordering = [f'translations__name']

class Car(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION
    trim = models.ForeignKey(
        Trim, on_delete=models.CASCADE, null=True, related_name="car_trims"
    )
    body = models.ForeignKey(
        Body, on_delete=models.CASCADE, null=True, related_name="bodies"
    )
    year = models.ManyToManyField(
        Year, related_name="cars", blank=True
    )

    def __str__(self):
        years_queryset = self.year.all()

        if years_queryset.exists():
            min_year = years_queryset.aggregate(models.Min('year'))['year__min']
            max_year = years_queryset.aggregate(models.Max('year'))['year__max']
            if max_year == min_year:
                years_str = max_year
            else:
                years_str = f"{min_year}-{max_year}"
        else:
            years_str = "No Year"
        
        return f"{years_str} {str(self.trim.model.make.name)} {str(self.trim.model.name)} {str(self.trim.name)} {str(self.body.name)}"

    def get_absolute_url(self):
        return reverse("portter:trim", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        try:
            years_queryset = self.year.all()
            if years_queryset.exists():
                min_year = years_queryset.aggregate(models.Min('year'))['year__min']
                max_year = years_queryset.aggregate(models.Max('year'))['year__max']
                years_str = f"{min_year} {max_year}"
            else:
                years_str = "No Year"
        except:
            years_str = ''
       
        slug_value = f"{years_str} {str(self.trim.model.make.name)} {str(self.trim.model.name)} {str(self.trim.name)}"

        self.slug = slugify(slug_value)

        super(Car, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        # ordering = [f'translations__name']

class Images(TranslatableModel, Extensions):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="cars")
    translations = DRY_TRANSLATION
    image = models.ImageField(
        upload_to=base_image_path,
        validators=[validate_image_extension],
        blank=True,
        null=True,
        help_text=_("Upload an image for the content."),
        verbose_name=_("Image"),
    )

    def __str__(self):
        return f"Image of {self.name} {self.car}"

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        # ordering = [f'translations__name']

class Files(Extensions):
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        help_text=_("Enter a slug for the content."),
        verbose_name=_("Slug"),
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_files")
    body_part = models.ForeignKey(
        BodyPart, on_delete=models.CASCADE, related_name="body_part_files"
    )
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True)

    file = models.FileField(
        upload_to=base_file_path_protected,
        blank=True,
        null=True,
        help_text=_("Upload a file for the content."),
        verbose_name=_("File"),
    )

    def __str__(self):
        return f"File of {self.slug}"

    def save(self, *args, **kwargs):
        # # Check if the file field has changed
        # if self.file and not self.width and not self.height:
        #     # Open the image using PIL
        #     img = Image.open(self.file.file)

        #     # Get the width and height of the image
        #     self.width = img.width
        #     self.height = img.height

        # if self.file and self.height and self.width:
        #     # Calculate and set the size
        #     self.size = self.width * self.height

        self.slug = slugify(
            f"{self.car.slug} {str(self.body_part.application.name)} {self.body_part.name}"
        )
        super(Files, self).save(*args, **kwargs)

    @property
    def file_url(self):
        try:
            url = self.file.url
        except:
            url = ""
        return url

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

