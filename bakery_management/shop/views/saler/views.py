from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shop.forms import CustomPasswordChangeForm
from shop.models import Order, Product
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Redirects to saler dashboard
class SaleHomeView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('saler_dashboard')

# Handles the saler dashboard page
class SalerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'saler/dashboard.html'
    
    def get(self, request):
        today = timezone.now().date()
        filter_date = datetime.combine(today, datetime.min.time())
        
        # Calculate daily revenue
        daily_revenue = Order.objects.filter(
            order_date__gte=filter_date, 
            order_date__lt=filter_date + timedelta(days=1)
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        # Handle product search
        search_query = request.GET.get('search', '')
        products = Product.objects.all().order_by('-availability', 'name')
        if search_query:
            products = products.filter(name__icontains=search_query)
        
        # Get orders of the day
        orders = Order.objects.filter(
            order_date__gte=filter_date, 
            order_date__lt=filter_date + timedelta(days=1)
        ).annotate(
            item_count=Count('items'),
            total_order_price=Sum('items__total_price')
        ).values('id', 'item_count', 'total_order_price', 'status')
        
        context = {
            'daily_revenue': daily_revenue,
            'products': products,
            'orders': orders,
            'search': search_query, 
        }
        return render(request, self.template_name, context)

# Handles product listing and search
class SaleProductView(LoginRequiredMixin, TemplateView):
    template_name = 'saler/product.html'
    
    def get(self, request, *args, **kwargs):
        products = self.get_products(request)
        return render(request, self.template_name, {'products': products})
    
    def get_products(self, request):
        product_list = Product.objects.all()
        
        # Handle product search
        search_query = request.GET.get('search', '')
        if search_query:
            product_list = product_list.filter(
                Q(name__icontains=search_query) | 
                Q(category__icontains=search_query) | 
                Q(flavor__icontains=search_query) 
            )

        # Pagination for products
        paginator = Paginator(product_list, 10) 
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 
        return page_obj

# Order view page (currently empty)
class SaleOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'saler/order_list.html'
    def get(self, request, *args, **kwargs):
        orders = self.get_orders(self.request)
        return render(self.request, self.template_name, {'orders': orders})
    def get_orders(self, request):
        order_list = Order.objects.all()
        search_query = request.GET.get('search', '')
        if search_query:
            order_list = order_list.filter(
                Q(order_date__icontains=search_query)       
            )
        paginator = Paginator(order_list, 10) 
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number)

        return page_obj
class SalerOrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'saler/order_detail.html'
    def get_context_data(self, **kwargs):
        order = self.get_order(kwargs['pk'])
        if not order:
            return render(self.request, '404.html', {'message': 'Order not found'})
        order_items = order.items.prefetch_related('product')
        context = {
            'order': order,
            'order_items': order_items,
        }
        return context
    def get_order(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

# Saler profile page
class SalerProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'saler/profile.html'
    def get(self, request, *args, **kwargs):
        saler = get_object_or_404(User, id= self.request.user.id)
        date_filter = request.GET.get('date', None)
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, "%Y-%m-%d")
                print(filter_date)
                orders = Order.objects.filter(saler=saler, order_date__date=filter_date.date())
            except ValueError:
                orders = Order.objects.filter(saler=saler)  # If the date format is incorrect, show all orders
        else:
            orders = Order.objects.filter(saler=saler)  # No date filter, show all orders
        
        return render(request, self.template_name, {'saler': saler, 'orders': orders})

# Create a new order for saler
class SalerMakeOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'saler/make_order.html'
    def get(self, request):
        return render(request, self.template_name)

# API for updating product availability (toggle between in-stock/out-of-stock)
class UpdateProductAvailability(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=HTTP_400_BAD_REQUEST)
        
        # Toggle product availability
        product.availability = not product.availability
        product.save()
        return Response({'detail': 'Product availability updated'}, status=HTTP_200_OK)
class ChangePasswordView(TemplateView):
    template_name = 'saler/change_password.html'
    
    def get(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            form.save(user) 
            update_session_auth_hash(request, user)  
            messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
            return redirect('saler_profile')
        else:
            messages.error(request, 'Đã xảy ra lỗi trong việc thay đổi mật khẩu!')
            return render(request, self.template_name, {'form': form})