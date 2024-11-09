from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('manager_home' if user.groups.filter(name='Quản lý').exists() else 'sale_home')
        else:
            error_message = 'Sai tên đăng nhập hoặc mật khẩu'
            return render(request, 'auth/login.html', {'error': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')
