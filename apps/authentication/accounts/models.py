import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'twitter': 'twitter', 'email': 'email'}

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

    # def create_manager(self, email, password=None):
    #     user = self.create_user(
    #         email=email,
    #         # full_name=full_name if full_name else email,
    #         password=password
    #     )

    #     user.is_admin = True
    #     user.is_staff = True
    #     user.save(using=self._db)

    #     return user

    # def create_employee(self, email, password=None):
    #     user = self.create_user(
    #         email=email,
    #         # full_name=full_name if full_name else email,
    #         password=password
    #     )

    #     user.is_admin = True
    #     user.is_staff = True
    #     user.save(using=self._db)

    #     return user

    def create_user_social(self, email=None, provider=None, social_id=None):
        if not provider and social_id:
            raise ValueError('Provider and social id is missing')
        user = self.model(
            email=self.normalize_email(email),
            provider=provider,
            social_id=social_id
        )
        user.is_verified = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # TODO Change to ID
    id = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, verbose_name='ID', editable=False, unique=True)
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'
    STATUS = [
        (ACTIVE, _('Active user')),
        (INACTIVE, _('User Inactive')),
        (DELETED, _('Soft Delete user')),
    ]

    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='email')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    verify_code = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(max_length=32, choices=STATUS, default=ACTIVE)
    auth_id = models.TextField(null=True, blank=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{str(self.first_name), str(self.last_name)}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name_plural = 'users'

    def get_user_info(self):
        return {
            'user_id': self.id,
            'email': self.email,
        }

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
