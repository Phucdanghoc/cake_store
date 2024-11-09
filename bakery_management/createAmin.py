import os
import django
from django.conf import settings

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Thông tin người dùng mới
admin_username = 'admin'  # Tên người dùng admin
admin_email = 'admin@admin.com'  # Địa chỉ email admin
admin_password = 'Admin123'  # Mật khẩu admin

admin_user = User.objects.create_user(username=admin_username, email=admin_email, password=admin_password)
admin_user.save()

manager_group = Group.objects.get(name='Quản lý')
manager_group.user_set.add(admin_user)

print(f"User '{admin_username}' has been created and added to the 'Manager' group.")

# Tạo tài khoản saler
saler_username = 'saler'  # Tên người dùng saler
saler_email = 'saler@saler.com'  # Địa chỉ email saler
saler_password = 'Saler123'  # Mật khẩu saler

# Tạo người dùng saler
saler_user = User.objects.create_user(username=saler_username, email=saler_email, password=saler_password)
saler_user.save()

# Thêm người dùng saler vào nhóm Nhân viên
saler_group = Group.objects.get(name='Nhân viên')
saler_group.user_set.add(saler_user)

print(f"User '{saler_username}' has been created and added to the 'Nhân viên' group.")
