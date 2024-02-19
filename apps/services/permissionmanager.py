from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.conf import settings
from django.db import models

from rest_framework import permissions as rest_permissions

class IsAdminUser(rest_permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)



# class PermissionGroup(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     permissions = models.ManyToManyField(Permission, related_name='permission_groups')

#     def __str__(self):
#         return self.name

# class UserPermission(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.user} - {self.permission}'


# class PermissionManager(models.Manager):
#     def __init__(self, model_class, tasks):
#         self.model_class = model_class
#         self.tasks = tasks
    
#     def get_permissions(self):
#         return [Permission.objects.get(codename=task) for task in self.tasks.__dict__.values()]

#     def assign_permissions(self, user, tasks):
#         permissions = [Permission.objects.get(codename=task) for task in tasks]
#         for permission in permissions:
#             UserPermission.objects.get_or_create(user=user, permission=permission)
    
#     def revoke_permissions(self, user, tasks):
#         permissions = [Permission.objects.get(codename=task) for task in tasks]
#         UserPermission.objects.filter(user=user, permission__in=permissions).delete()

#     def has_permission(self, user, task):
#         permission = Permission.objects.get(codename=task)
#         return UserPermission.objects.filter(user=user, permission=permission).exists()

# # class Model1(models.Model):
# #     # fields
    
# #     permission_manager = PermissionManager(Model1, Tasks.Model1)

# # manager_role, _ = Group.objects.get_or_create(name='Manager')
# # manager_role.permissions.set(
# #     PermissionManager(Model1, Tasks.Model1).get_permissions() + 
# #     PermissionManager(Model2, Tasks.Model2).get_permissions()
# # )

# # user = User.objects.get(id=1)
# # manager_role.permission_manager.assign_permissions(user, [Tasks.Model1.CREATE, Tasks.Model2.UPDATE])
# # manager_role.permission_manager.revoke_permissions(user, [Tasks.Model1.UPDATE, Tasks.Model2.READ])

# # user = User.objects.get(id=1)
# # has_permission = manager_role.permission_manager.has_permission(user, Tasks.Model1.CREATE)
