from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
import openpyxl
from rest_framework import serializers
from shop.forms import ExcelUploadForm, ProductForm
from shop.models import Product
from django.db.models import Q
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response



class AddProductView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/product/add_product.html'
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        excel_form = ExcelUploadForm()
        return render(request, self.template_name, {'form': form, 'excel_form': excel_form})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm sản phẩm thành công!')
            return redirect('product_list')
        else:
            messages.error(request, 'Thông tin không hợp lệ.')
            return render(request, self.template_name, {'form': form})

class ExcelUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/product/add_product.html'

    def post(self, request, *args, **kwargs):
        if 'submit_excel' in request.POST:
            excel_form = ExcelUploadForm(request.POST, request.FILES)
            if excel_form.is_valid():
                file = request.FILES['excel_file']
                try:
                    self.import_products_from_excel(file)
                    messages.success(request, 'Sản phẩm đã được nhập thành công từ Excel.')
                except Exception as e:
                    messages.error(request, f'Lỗi khi nhập sản phẩm: {e}')
                return redirect('product_list')
            else:
                messages.error(request, 'Vui lòng chọn tệp Excel.')
                print(excel_form.errors)
                return render(request, self.template_name, {'excel_form': excel_form})
        return redirect('product_list')

    def import_products_from_excel(self, file):
        wb = openpyxl.load_workbook(file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            name, price, category, description, image_url, availability, flavor, size = row
            if availability == "Có sẵn":
                availability = True
            else:
                availability = False
            Product.objects.create(
                name=name,
                price=price,
                category=category,
                description=description,
                image_url=image_url,
                availability=availability,
                flavor=flavor,
                size=size
            )
class ProductListView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/product/product_list.html'

    def get(self, request, *args, **kwargs):
        products = self.get_products(request)
        return render(request, self.template_name, {'products': products})

    def get_products(self, request):
        product_list = Product.objects.all()
        search_query = request.GET.get('search', '')
        if search_query:
            product_list = product_list.filter(
                Q(name__icontains=search_query) | 
                Q(category__icontains=search_query) | 
                Q(flavor__icontains=search_query) 
            )

        paginator = Paginator(product_list, 10) 
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 
        return page_obj

class EditProductView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/product/edit_product.html'

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['pk'])
        form = ProductForm(instance=product)
        return render(request, self.template_name, {'form': form, 'product': product})

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['pk'])
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'There was an error updating the product. Please try again.')
        return render(request, self.template_name, {'form': form, 'product': product})
class DeleteProductView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/product/delete_product.html'

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['pk'])
        return self.render_to_response({'product': product})

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['pk'])
        try:
            product.delete()
            messages.success(request, 'Product deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting product: {e}')
        return redirect('product_list')


class ProductAPI(APIView):
    def get(self, request):
            search_query = request.GET.get('name', None)
            if search_query:
                products = Product.objects.filter(name__icontains=search_query)
            else:
                products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'flavor', 'size', 'image_url', 'availability'] 
        depth = 1