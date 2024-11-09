from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from shop.forms import SalerForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime

from shop.models import Order




class SalerListView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/saler/saler_list.html'
    
    def get(self, request, *args, **kwargs):
        salers = self.get_salers(request)
        return render(request, self.template_name, {'salers': salers})
    def get_salers(self, request):
        salers = User.objects.filter(groups__name='Nhân viên')
        search_query = request.GET.get('search', '')
        if search_query:
            salers = salers.filter(
                Q(username__icontains=search_query)
            )
        paginator = Paginator(salers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)    
        return page_obj


class SalerCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/saler/add_saler.html'
    
    def get(self, request, *args, **kwargs):
        form = SalerForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = SalerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.split('@')[0]
            user.password = make_password(user.username) 
            user.save()
            try:
                group = Group.objects.get(name='Nhân viên')
                group.user_set.add(user)
            except Group.DoesNotExist:
                messages.error(request, 'Không tìm thấy nhóm "Nhân viên"')
                return redirect('saler_list')
            messages.success(request, 'Thêm nhân viên thanh cong!')
            return redirect('saler_list')
        
        
        messages.error(request, 'There was an error adding the saler. Please try again.')
        return render(request, self.template_name, {'form': form})
        


class EditSalerView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/saler/edit_saler.html'
    
    def get(self, request, *args, **kwargs):
        saler = User.objects.get(id=kwargs['pk'])
        form = SalerForm(instance=saler)
        return render(request, self.template_name, {'form': form, 'saler': saler})
    
    def post(self, request, *args, **kwargs):
        saler = User.objects.get(id=kwargs['pk'])
        form = SalerForm(request.POST, instance=saler)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thanh cong!')
            return redirect('saler_list')
        else:
            messages.error(request, 'Lỗi trong khi cập nhật saler.')
        return render(request, self.template_name, {'form': form, 'saler': saler})
class ResetPasswordView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        saler = User.objects.get(id=kwargs['pk'])
        new_password = saler.email.split('@')[0]
        saler.set_password(new_password)
        saler.save()
        messages.success(request, f'Password reset successfully! New password: {new_password}')
        return redirect('saler_detail', pk=saler.id)  

class SalerDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/saler/delete_saler.html'   
    def get(self, request, *args, **kwargs):
        saler = User.objects.get(id=kwargs['pk'])   
        return render(request, self.template_name, {'saler': saler})
    def post(self, request, *args, **kwargs):
        saler = User.objects.get(id=kwargs['pk'])
        try:
            saler.delete()
            messages.success(request, 'Xóa thành cong!')
        except Exception as e:
            messages.error(request, f'Lỗi xóa : {e}')
        return redirect('saler_list')    
    
class SalerUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/saler/update_saler.html'
    def get(self, request, *args, **kwargs):
        saler = User.objects.get(id=kwargs['pk'])
        form = SalerForm(instance=saler)
        return render(request, self.template_name, {'form': form, 'saler': saler})
    def post(self, request, *args, **kwargs):
        saler = User.objects.get(id=kwargs['pk'])        
        form = SalerForm(request.POST, instance=saler)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành cong!')
            return redirect('saler_list')
        else:
            messages.error(request, 'Thông tin không hợp lệ!')
        return render(request, self.template_name, {'form': form, 'saler': saler})
class DetailSalerView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/saler/detail_saler.html'
    def get(self, request, *args, **kwargs):
        saler = get_object_or_404(User, id=kwargs['pk'])
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
