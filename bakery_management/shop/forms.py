from django import forms
from .models import Product, Promotion
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
import re
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image_url', 'availability', 'flavor', 'size']
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()



class SalerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class PromotionForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Promotion
        fields = ['name', 'discount_type', 'discount_value', 'start_date', 'end_date']
class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Mật khẩu cũ",
        required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Mật khẩu mới",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Xác nhận mật khẩu mới",
        required=True
    )

    def clean_new_password2(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Mật khẩu mới không khớp với xác nhận mật khẩu!")
        
        return confirm_password

    def save(self, user):
        user.set_password(self.cleaned_data['new_password'])
        user.save()
        return user