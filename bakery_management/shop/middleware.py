from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404

class AccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kiểm tra nếu người dùng chưa đăng nhập và đang truy cập trang chủ
        if request.path == "/" and not self.is_auth(request):
            return redirect(reverse('login'))

        # Kiểm tra quyền truy cập cho từng nhóm
        if self.is_auth(request):
            if self.is_saler(request) and request.path.startswith('/manager'):
                return redirect(reverse('sale_home'))
            if self.is_manager(request):
                pass

        # Kiểm tra xem trang có tồn tại hay không, nếu không thì trả về trang 404
        try:
            response = self.get_response(request)
        except Http404:
            return render(request, 'auth/404.html')  # Render trang 404 nếu không tìm thấy trang
        return response

    def is_auth(self, request):
        """Kiểm tra nếu người dùng đã đăng nhập."""
        return request.user.is_authenticated

    def is_manager(self, request):
        """Kiểm tra nếu người dùng thuộc nhóm 'Quản lý'."""
        return request.user.groups.filter(name='Quản lý').exists()

    def is_saler(self, request):
        """Kiểm tra nếu người dùng thuộc nhóm 'Nhân viên'."""
        return request.user.groups.filter(name='Nhân viên').exists()
