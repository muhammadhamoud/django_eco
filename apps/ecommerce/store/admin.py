from django.contrib import admin


# from django.forms import inlineformset_factory
from .models import (
    Product, ProductImage, Category, ProductFile, ProductViews, ProductPrice, ProductLabel, Currency, Coupon, ProductReview, CartItem, Order, Reservation
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1

class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductFileInline,
        ProductPriceInline,
    ]
    list_display = ['name', 
                    'is_active',
                    'is_deleted',
                    'is_digital',
                    'is_featured',
                    'is_new_arrival',
                     'created', 'stock']
    list_filter = ['stock', 'created']
    list_editable = ['stock', 'is_active',
                    'is_deleted',
                    'is_digital',
                    'is_featured',
                    'is_new_arrival']
    
    # prepopulated_fields = {'translations__name': ('slug',)}

# Register the models with their respective admins
# admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

# Customize the admin for other models as needed
admin.site.register(ProductImage)
admin.site.register(ProductFile)
admin.site.register(ProductViews)
admin.site.register(ProductPrice)
admin.site.register(ProductLabel)
admin.site.register(Currency)
admin.site.register(Coupon)
admin.site.register(ProductReview)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Reservation)
