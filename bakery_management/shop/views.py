from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# class LoginView(View):
#     def get(self, request):
#         return render(request, 'auth/login.html')

#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('manager_home' if user.groups.filter(name='Quản lý').exists() else 'sale_home')
#         else:
#             messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu')
#             return render(request, 'auth/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')  

# class AddProductView(PermissionRequiredMixin, View):
#     permission_required = 'shop.add_product'
#     raise_exception = True

#     def get(self, request):
#         return render(request, 'add_product.html')

# class CreateOrderView(PermissionRequiredMixin, View):
#     permission_required = 'shop.add_order'
#     raise_exception = True

#     def get(self, request):
#         return render(request, 'create_order.html')

# class ViewOrdersView(PermissionRequiredMixin, TemplateView):
#     permission_required = 'shop.view_order'
#     raise_exception = True
#     template_name = 'view_orders.html'


# class ManagerHomeView(LoginRequiredMixin, View):
#     def get(self, request):
#         return render(request, 'manager/index.html')


# class SaleHomeView(LoginRequiredMixin, View):
#     def get(self, request):
#         return render(request, 'saler/index.html') 

