from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

from core.handle_images import compress_image
from core.models import DRY_TRANSLATION_SHOP, BaseContentShop

# class Category(models.Model):
#     pass

class Product(models.Model):
    pass

class Category(TranslatableModel, BaseContentShop):
    translations = DRY_TRANSLATION_SHOP
    # name = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        # ordering = ["translations__name"]
        # indexes = [
        #     models.Index(fields=["translations__name"]),
        # ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


# class Product(models.Model):
#     category = models.ForeignKey(
#         Category, related_name="products", on_delete=models.CASCADE
#     )
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     available = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)

#     class Meta:
#         ordering = ["name"]
#         indexes = [
#             models.Index(fields=["id", "slug"]),
#             models.Index(fields=["name"]),
#             models.Index(fields=["-created"]),
#         ]

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("shop:product_detail", args=[self.id, self.slug])
    
#     def save(self, *args, **kwargs):
		
#         # Check if the image field is not None and has a file associated with it
#         if self.image and not self.image.name:
#             self.image = compress_image(self.image)
        
#         # Update the slug using the name field
#         # self.slug = slugify(self.name)
#         super(Product, self).save(*args, **kwargs)
