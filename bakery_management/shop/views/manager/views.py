from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
import openpyxl
from shop.forms import ExcelUploadForm, ProductForm
from shop.models import Product
from django.db.models import Q
from django.contrib import messages

class ManagerHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/base.html'

    def get(self, request, *args, **kwargs):
        return redirect('product_list')




