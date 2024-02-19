from rest_framework import serializers
from cart.models import Cart, Cartitems
from store.models import Product
from store.api.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model= Cartitems
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def total(self, cartitem:Cartitems):
        return cartitem.quantity * cartitem.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value
    
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"] 
        quantity = self.validated_data["quantity"] 
        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except:
            self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = Cartitems
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cartitems
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')
    
    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total







# class CartProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = (
#             "title",
#             "seller",
#             "quantity",
#             "price",
#             "image",
#         )


# class CartItemSerializer(serializers.ModelSerializer):
#     # product = CartProductSerializer(required=False)
#     class Meta:
#         model = CartItem
#         fields = ["cart", "product", "quantity"]


# class CartItemMiniSerializer(serializers.ModelSerializer):
#     product = CartProductSerializer(required=False)

#     class Meta:
#         model = CartItem
#         fields = ["product", "quantity"]


# class CartItemUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ["product", "quantity"]

