from datetime import datetime, timezone, timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
import phonenumbers
from core.models import TimeStampedModel
from django.conf import settings

# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException
# from randompinfield import RandomPinField

# from .signals import register_signal
# from .managers import NationalIDImageManager
# from core.handle_images import compress_image

User = settings.AUTH_USER_MODEL


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return "users/{0}/{1}".format(instance.user.id, filename)


def national_image_path(instance, filename):
    return f"national/{instance.user.username}/images/{filename}"


class Profile(TimeStampedModel):
    GENDER_MALE = "m"
    GENDER_FEMALE = "f"
    OTHER = "o"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (OTHER, "Other"),
    )
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    about = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    @property
    def last_seen(self):
        return cache.get(f"seen_{self.user}")

    @property
    def online(self):
        if self.last_seen:
            now = datetime.now(timezone.utc)
            if now > self.last_seen + timedelta(minutes=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Address(TimeStampedModel):
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    country = CountryField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    building_number = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
    apartment_number = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.user}"

@receiver(post_save, sender=User)
def create_address(sender, instance, created, *args, **kwargs):
    if created:
        Address.objects.create(user=instance)
