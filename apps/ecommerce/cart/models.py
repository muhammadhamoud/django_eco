from django.db import models
from core.models import TimeStampedModel
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from store.models import Product


class Cart(TimeStampedModel):

    def __str__(self):
        return str(self.id)

class Cartitems(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)






















# class Cart(TimeStampedModel):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name="user_cart", on_delete=models.SET_NULL, null=True, blank=True
#     )
#     session_key = models.CharField(max_length=40, blank=True, null=True)
    
#     total = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0, blank=True, null=True
#     )

#     def __str__(self) -> str:
#         return str(self.session_key)

#     @classmethod
#     def get_cart(cls, user, session_key):
#         return cls.objects.filter(Q(user=user) | Q(session_key=session_key)).first()
    


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_cart(sender, created, instance, *args, **kwargs):
#     if created:
#         if not instance.is_anonymous:
#             # For authenticated users, update their session_key
#             session = SessionStore()
#             session.create()
#             instance.session_key = session.session_key
#             instance.save()
    
#     # Create or retrieve a cart for the user or session key
#     Cart.objects.get_or_create(user=instance, session_key=instance.session_key)


# class CartItem(TimeStampedModel):
#     cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, related_name="cart_product", on_delete=models.CASCADE
#     )
#     quantity = models.IntegerField(default=1)

# from django.db import models
# from core.models import TimeStampedModel
# from django.contrib.auth import get_user_model
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from products.models import Product
# from django.conf import settings

# class Cart(TimeStampedModel):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name="user_cart", on_delete=models.SET_NULL, null=True
#     )

#     session_key = models.CharField(max_length=40, blank=True, null=True)

#     total = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0, blank=True, null=True
#     )


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_cart(sender, created, instance, *args, **kwargs):
#     if created:
#         Cart.objects.create(user=instance)


# class CartItem(TimeStampedModel):
#     cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, related_name="cart_product", on_delete=models.CASCADE
#     )
#     quantity = models.IntegerField(default=1)

