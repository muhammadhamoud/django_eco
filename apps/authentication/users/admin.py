from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from django.contrib import admin
from .models import CustomUser

class GroupInline(admin.TabularInline):
    model = CustomUser.groups.through
    extra = 1
    verbose_name_plural = 'groups'

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_admin', 'is_verified', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin', 'is_superuser','is_verified', 'status')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Social Users', {'fields': ('auth_id','auth_provider')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1','password2','first_name', 'last_name', 'is_staff', 'is_active', 'is_admin', 'is_superuser','is_verified'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups',)

    inlines = (GroupInline,)

admin.site.register(CustomUser, UserAdmin)