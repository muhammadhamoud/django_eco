from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, Extensions
from mptt.models import MPTTModel, TreeForeignKey


def category_image_path(instance, filename):
    return "category/icons/{}/{}".format(instance.name, filename)


def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)


class Category(MPTTModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("Enter the name of the category."),
    )
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(Extensions):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=product_image_path, blank=True)
    
    views = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_product", on_delete=models.CASCADE
    )
    category = TreeForeignKey(
        Category, related_name="product_category", on_delete=models.CASCADE
    )


    def __str__(self):
        return str(self.uuid)


class Pricing(Extensions):
    pass


class ProductViews(TimeStampedModel):
    ip = models.CharField(max_length=250)
    product = models.ForeignKey(
        Product, related_name="product_views", on_delete=models.CASCADE
    )

class Purchase(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)


# @receiver(post_save, sender=Product)
# def create_index_elasticsearch(sender, instance, *args, **kwargs):
#     post_signal(sender, instance)
#     from .serializers import ProductDocumentSerializer
#     serializer = ProductDocumentSerializer(instance)
#     serializer.save()