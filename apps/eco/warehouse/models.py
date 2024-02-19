from datetime import date, timedelta
from django.db import models
from django.utils.translation import gettext as _
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from parler.models import TranslatableModel, TranslatedFields, TranslatedField
from core.models import TimeStampedModel, Extensions, ModelExtensions, IncrementingIntegerField, BaseContent, DRY_TRANSLATION, PrimaryKeyUUID, DRY_TRANSLATION_SHOP, BaseContentShop
from core.models import base_image_path, validate_image_extension, custom_upload_path

END_DATE = settings.END_DATE

class Attribute(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("store:attribute", kwargs={'id': self.id})


class Tag(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("store:tag", kwargs={'id': self.id})


class Category(TranslatableModel, BaseContentShop):
    translations = DRY_TRANSLATION_SHOP
    tag = models.ManyToManyField(Tag, related_name='tags', blank=True)
    attribute = models.ManyToManyField(Attribute, related_name='attributes', blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['translations__name']

    def __str__(self):
        return str(self.name)


class ProductLabel(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("store:label", kwargs={'id': self.id})

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Coupon(TimeStampedModel):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(
        max_digits=5, decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
        )
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = _('Price Coupon')
        verbose_name_plural = _('Price Coupons')

class Product(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION
    category = models.ForeignKey(Category, related_name="product_category", on_delete=models.CASCADE)
    label = models.ForeignKey(ProductLabel, on_delete=models.CASCADE, related_name='labels')
    stock = models.PositiveIntegerField(default=1000)
    views = models.IntegerField(default=0)
    average_rating = models.IntegerField(default=0)
    purchases = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=True, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('store:product', args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", args=[str(self.id)])

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Check if the product is being created (not updating)
        is_new_product = not self.pk

        super(Product, self).save(*args, **kwargs)

        if is_new_product:
            # Create a default product price upon creating a new product
            currency = Currency.objects.get(code="JOR") 
            default_price = ProductPrice(product=self, currency=currency, price=999.00)  # Set your default price here
            default_price.save()

    @property
    def review_count(self):
        return self.reviews.count()


class ProductImage(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
		upload_to=base_image_path,
		validators=[validate_image_extension],
		blank=True,
		null=True,
		help_text=_("Upload an image for the content."),
		verbose_name=_("Image")
	)

    def __str__(self):
        return f"Image of {self.name}"

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class ProductPrice(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="currencies")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_discounted = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=END_DATE)

    PERIOD_CHOICES = (('D', _('Daily')), ('W', _('Weekly')), ('M', _('Monthly')),)

    period = models.CharField(max_length=1, choices=PERIOD_CHOICES, default='D')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name="coupons")

    def __str__(self):
        return f"{self.product.name} - {self.get_period_display()} Price: {self.price}"

    class Meta:
        verbose_name = _('Product Price')
        verbose_name_plural = _('Product Prices')


class ProductViews(TimeStampedModel):
    ip_address = models.CharField(max_length=250)
    product = models.ForeignKey(Product, related_name="product_views", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Product View')
        verbose_name_plural = _('Product Views')


class ProductPurchaseCount(TimeStampedModel):
    payment_id = models.CharField(max_length=250)
    product = models.ForeignKey(Product, related_name="product_purchase", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Purchase Count')
        verbose_name_plural = _('Purchase Counts')


class ProductFile(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_files")
    file = models.FileField(upload_to=custom_upload_path)


class ProductReview(TimeStampedModel):
    # Define choices for rating
    RATING_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')

    def __str__(self):
        return f"{self.user} - {self.product.translations.name}"


class CartItem(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_item_user")
    item = models.ForeignKey(ProductPrice, on_delete=models.CASCADE, related_name='cart_itmes', blank=True, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.product.translations.name}"

    def add_to_cart(self, productprice):
        self.item = productprice
        self.save()

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.price_discounted

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.price_discounted:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user")
    items = models.ManyToManyField(CartItem)

    ref_code = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    # shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    # billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()  # if self.coupon:  #     total -= self.coupon.amount  # return total


class Reservation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservation_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reservation')
    currency = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_discounted = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default="booked")
    confirmation = IncrementingIntegerField()

    def __str__(self):
        return f"{self.product.translations.name} for {self.user.email} - CONFO: {self.confirmation}"


