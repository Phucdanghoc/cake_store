from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from shop.forms import PromotionForm
from shop.models import Promotion
from django.contrib import messages

class PromotionListView(LoginRequiredMixin,TemplateView):
    template_name = 'manager/promotion/promotion_list.html' 
    def get(self, request, *args, **kwargs):
        promotions = self.get_promotions(request)
        return render(request, self.template_name, {'promotions': promotions})
    
    def get_promotions(self, request: HttpRequest) -> Any:
        promotions = Promotion.objects.all()
        search_query = request.GET.get('q')
        if search_query:
            promotions = promotions.filter(name__icontains=search_query)
        paginator = Paginator(promotions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
    
class PromotionCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/promotion/create_promotion.html'

    def get(self, request, *args, **kwargs):
        form = PromotionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.save()
            messages.success(request, 'Promotion added successfully!')
            return redirect('promotion_list')
        else:
            messages.error(request, 'There was an error adding the promotion. Please try again.')
        
        return render(request, self.template_name, {'form': form})
class PromotionUpdateView(LoginRequiredMixin,TemplateView):
    template_name = 'manager/promotion/promotion_update.html'
    def get(self, request, *args, **kwargs):
        promotion = get_object_or_404(Promotion, id=kwargs['pk'])
        form = PromotionForm(instance=promotion)
        return render(request, self.template_name, {'form': form, 'promotion': promotion})
    
    def post(self, request, *args, **kwargs):
        promotion = get_object_or_404(Promotion, id=kwargs['pk'])
        form = PromotionForm(request.POST, instance=promotion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promotion updated successfully!')
            return redirect('promotion_list')
        else:
            messages.error(request, 'There was an error updating the promotion. Please try again.')

class PromotionDeleteView(LoginRequiredMixin,TemplateView):
    template_name = 'manager/promotion/promotion_delete.html'
    def get(self, request, *args, **kwargs):
        promotion = get_object_or_404(Promotion, id=kwargs['pk'])
        return render(request, self.template_name, {'promotion': promotion})
    
    def post(self, request, *args, **kwargs):
        promotion = get_object_or_404(Promotion, id=kwargs['pk'])
        try :
            promotion.delete()
            messages.success(request, 'Promotion deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting promotion: {e}')
       
        return redirect('promotion_list')