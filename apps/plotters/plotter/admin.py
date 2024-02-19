from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline, TranslatableStackedInline
from parler.admin import SortedRelatedFieldListFilter
from .models import *

# Define the get_prepopulated_fields method for all inline classes
def get_prepopulated_fields(self, request, obj=None):
    return {'slug': ('name',)}

def get_prepopulated_car_fields(self, request, obj=None):
    return {'slug': ('trim',)}

@admin.register(Application)
class ApplicationAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['translations__name']

@admin.register(Make)
class MakeAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['translations__name']

@admin.register(Trim)
class TrimAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['translations__name']

@admin.register(Body)
class BodyAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['translations__name']

@admin.register(BodyPart)
class BodyPartAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['translations__name']

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    pass

@admin.register(Height)
class HeightAdmin(admin.ModelAdmin):
    pass

@admin.register(Width)
class WidthAdmin(admin.ModelAdmin):
    pass

@admin.register(PlotterMachine)
class PlotterMachineAdmin(admin.ModelAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['name', 'slug']

@admin.register(Car)
class CarAdmin(TranslatableAdmin):
    # get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['translations__name', 'translations__slug']

@admin.register(Model)
class ModelAdmin(TranslatableAdmin):
    get_prepopulated_fields = get_prepopulated_fields
    search_fields = ['translations__name']


@admin.register(Images)
class ImagesAdmin(TranslatableAdmin):
    pass

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    pass


