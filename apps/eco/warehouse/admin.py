from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline, TranslatableStackedInline

# from django.forms import inlineformset_factory
from .models import (
    Product, ProductImage, Category, ProductFile, ProductViews, ProductPrice, ProductLabel, Currency, Coupon, ProductReview, CartItem, Order, Attribute, Tag
)

# Define the get_prepopulated_fields method for all inline classes
def get_prepopulated_fields(self, request, obj=None):
    return {'slug': ('name',)}

# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1

# class ProductFileInline(admin.TabularInline):
#     model = ProductFile
#     extra = 1

# class ProductPriceInline(admin.TabularInline):
#     model = ProductPrice
#     extra = 1

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         ProductImageInline,
#         ProductFileInline,
#         ProductPriceInline,
#     ]
#     list_display = ['name', 
#                     'is_active',
#                     'is_deleted',
#                     'is_digital',
#                     'is_featured',
#                     'is_new_arrival',
#                      'created', 'stock']
#     list_filter = ['stock', 'created']
#     list_editable = ['stock', 'is_active',
#                     'is_deleted',
#                     'is_digital',
#                     'is_featured',
#                     'is_new_arrival']
    
    # prepopulated_fields = {'translations__name': ('slug',)}

# Register the models with their respective admins
# admin.site.register(Product, ProductAdmin)
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']  # Directly reference translated fields
    get_prepopulated_fields = get_prepopulated_fields
    # Define other customizations for the admin interface as needed
    search_fields = ['translations__name', 'translations__slug', 'translations__description']

@admin.register(Attribute)
class AttributeAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    
@admin.register(Tag)
class TagAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    

# @admin.register(Product)
# class ProductAdmin(TranslatableAdmin):
#     get_prepopulated_fields = get_prepopulated_fields


# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     pass

# @admin.register(ProductPrice)
# class ProductPriceAdmin(admin.ModelAdmin):
#     pass

@admin.register(ProductFile)
class ProductFileAdmin(admin.ModelAdmin):
    pass
    
@admin.register(ProductViews)
class ProductViewsAdmin(admin.ModelAdmin):
    pass
    

    
@admin.register(ProductLabel)
class ProductLabelAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass
    
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
  
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

# @admin.register(CartItem)
# class CartItemAdmin(TranslatableAdmin):
#     get_prepopulated_fields = get_prepopulated_fields
    
# @admin.register(Order)
# class OrderAdmin(TranslatableAdmin):
#     get_prepopulated_fields = get_prepopulated_fields
    
# @admin.register(Reservation)
# class ReservationAdmin(TranslatableAdmin):
#     get_prepopulated_fields = get_prepopulated_fields



class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    inlines = [ProductPriceInline, ProductImageInline]
    list_display = ['name', 'category', 'stock', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['translations__name', 'category__translations__name']

admin.site.register(ProductPrice)
admin.site.register(ProductImage)