from django.contrib import admin
from django.shortcuts import render
from .models import Category, Product

admin.site.register(Category)
# admin.site.register(Product)

# from .models import ProductViews
# admin.site.register(ProductViews)


from django import forms

class ChangeImageURLForm(forms.Form):
    new_image_url = forms.URLField(label="New Image URL")

from django.contrib import admin


def change_image_urls(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = ChangeImageURLForm(request.POST)
        if form.is_valid():
            new_image_url = form.cleaned_data['new_image_url']
            for product in queryset:
                product.image = new_image_url
                product.save()
            modeladmin.message_user(request, f"Image URLs updated for {queryset.count()} products.")
    else:
        form = ChangeImageURLForm()

    return render(request, "admin/change_image_url.html", {"form": form})

change_image_urls.short_description = "Change Image URLs for Selected Products"

from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    actions = [change_image_urls]

# Register the Product model with the custom admin class
admin.site.register(Product, ProductAdmin)