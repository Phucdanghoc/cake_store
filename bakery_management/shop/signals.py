from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.apps import AppConfig

def create_groups(sender, **kwargs):
    manager_group, _ = Group.objects.get_or_create(name='Quản lý')
    permissions = ['can_add_product', 'can_edit_product', 'can_delete_product', 'can_view_orders']
    for perm in permissions:
        try:
            permission = Permission.objects.get(codename=perm)
            manager_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission '{perm}' does not exist and was not added to the 'Quản lý' group.")

    staff_group, _ = Group.objects.get_or_create(name='Nhân viên')
    staff_permissions = ['can_view_products', 'can_create_order']
    for perm in staff_permissions:
        try:
            permission = Permission.objects.get(codename=perm)
            staff_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission '{perm}' does not exist and was not added to the 'Nhân viên' group.")
def register_signals():
    post_migrate.connect(create_groups)
