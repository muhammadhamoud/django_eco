from rest_framework import serializers
from datetime import date, timedelta
from store.models import (
    Category, Product, ProductLabel, ProductImage, 
    Currency, ProductPrice, ProductViews, ProductFile,
    ProductPurchaseCount, Coupon, ProductReview, CartItem,
    Order, Reservation
)
from store.models import END_DATE

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    # Define any fields to be excluded in all serializers
    exclude_fields = []

    def get_field_names(self, declared_fields, info):
        fields = super(BaseSerializer, self).get_field_names(declared_fields, info)
        return [field for field in fields if field not in self.exclude_fields]
  
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("modified",)

class ProductLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLabel
        exclude = ("modified",)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"
        # exclude = ("modified",)

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"

class ProductPriceSerializer(serializers.ModelSerializer):
    #TODO change the end date values automatically daily END_DATE
    currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        many=False,
        write_only=True,
        required=True,
        label='Currency'
    )
    coupon = serializers.PrimaryKeyRelatedField(
        queryset=Coupon.objects.all(),
        many=False,
        write_only=True,
        required=False,
        allow_null=True,
        label='Coupon'
    )
    start_date = serializers.DateField(default=date.today(), format="%Y-%m-%d")
    end_date = serializers.DateField(default=date.today() + timedelta(days=366), format="%Y-%m-%d")

    class Meta:
        model = ProductPrice
        exclude = ("modified",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Format the dates to "YYYY-MM-DD" format
        representation['start_date'] = instance.start_date.strftime("%Y-%m-%d")
        representation['end_date'] = instance.end_date.strftime("%Y-%m-%d")
        representation['currency'] = CurrencySerializer(instance.currency).data
        representation['coupon'] = CouponSerializer(instance.coupon).data

        return representation
    
    def get_fields(self):
        fields = super().get_fields()

        # Set the initial values for the fields
        fields['start_date'].initial = self.default_start_date()
        fields['end_date'].initial = self.default_end_date()

        return fields

    def default_start_date(self):
        return (date.today()).strftime("%Y-%m-%d")

    def default_end_date(self):
        return END_DATE.strftime("%Y-%m-%d")

class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        exclude = ("modified",)

class ProductPurchaseCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPurchaseCount
        exclude = ("modified",)

class ProductFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFile
        exclude = ("modified",)

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        exclude = ("modified",)

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, required=False)
    prices = ProductPriceSerializer(many=True, required=False)
    reviews = ProductReviewSerializer(many=True, required=False)

    # views = ProductViewsSerializer(many=True)
    # files = ProductFileSerializer(many=True)

    class Meta:
        model = Product
        exclude = ("modified",)


    def get_category(self, obj):
        return obj.category.name
    
    def get_label(self, obj):
        return obj.label.name
    
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("modified",)

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        exclude = ("modified",)


class CartItemSerializer(serializers.ModelSerializer):
    prices = ProductSerializer(many=True, required=False)
    class Meta:
        model = CartItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    items = CartItemSerializer(many=True, required=False)
    class Meta:
        model = Order
        fields = "__all__"

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

