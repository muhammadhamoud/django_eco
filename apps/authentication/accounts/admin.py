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
        ('Personal info', {'fields': ('first_name', 'last_name')}),
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




# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth import get_user_model

# UserModel = get_user_model()

# class CustomUserAdmin(BaseUserAdmin):
#     fieldsets = (
#         # ... other fieldsets ...
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         # ... other add_fieldsets ...
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     list_display = ('email', 'is_staff')
#     search_fields = ('email')
#     ordering = ('email',)

#     # remove filter_horizontal setting for groups
#     filter_horizontal = ()


# from django.contrib.auth.models import Group

# class GroupInline(admin.TabularInline):
#     model = UserModel.groups.through
#     extra = 1

# class UserAdmin(BaseUserAdmin):
#     inlines = (GroupInline,)

# admin.site.unregister(UserModel)
# admin.site.register(UserModel, UserAdmin)


# # from django.contrib import admin
# # from django.contrib.auth.models import Group
# # from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# # from django.contrib.auth.models import User

# # # Register your models here.
# # user = get_user_model()

# # class AccessTokensAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'user_id', 'access_token', 'created_at', 'expired_at']


# # class RefreshTokensAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'refresh_token', 'access_token_id', 'created_at', 'expired_at']



# # # from django.contrib import admin
# # # from django.contrib.auth.models import Group
# # # from django.contrib.auth import get_user_model
# # # from . import models

# # # from django.contrib import admin
# # # from django.contrib.auth import get_user_model
# # # from django.contrib.auth.admin import UserAdmin
# # # from django import forms

# # # # user = get_user_model()

# # class CustomUserCreationForm(forms.ModelForm):
# #     password = None

# #     class Meta:
# #         model = get_user_model()
# #         fields = ('email', 'is_active', 'is_staff', 'is_admin') #('email', 'is_active', 'is_staff', 'is_admin', 'is_verified')

# # class CustomUserChangeForm(forms.ModelForm):
# #     password = None

# #     class Meta:
# #         model = get_user_model()
# #         fields = fields = ('email', ) #('email', 'is_active', 'is_staff', 'is_admin', 'is_verified')

# # class CustomUserAdmin(UserAdmin):
# #     add_form = CustomUserCreationForm
# #     form = CustomUserChangeForm

# # # # admin.site.unregister(get_user_model())
# # # admin.site.register(get_user_model(), CustomUserAdmin)





# # class CustomUserAdmin(UserAdmin):
# #     fieldsets = (
# #         # ... other fieldsets ...
# #         ('Permissions', {'fields': ('is_staff', 'is_active')}),
# #     )
# #     add_fieldsets = (
# #         # ... other add_fieldsets ...
# #         ('Permissions', {'fields': ('is_staff', 'is_active')}),
# #     )
# #     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
# #     search_fields = ('username', 'email', 'first_name', 'last_name')
# #     ordering = ('username',)
    
# #     # remove filter_horizontal setting for groups
# #     filter_horizontal = ()






# # admin.site.unregister(User)
# # admin.site.register(user, CustomUserAdmin)

# # # admin.site.unregister(Group)
# # # admin.site.register(user, UserAdmin)

# # # # admin.site.unregister(Group)
# # # from django.contrib.auth.models import User
# # # admin.site.register(User, UserAdmin)
# # # # admin.site.register(user)

# # # # admin.site.register(AccessTokensAdmin)

# # # # Register CustomUser with UserAdmin
# # # # admin.site.register(UserAdmin)