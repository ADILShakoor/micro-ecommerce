# from typing import Any, Mapping
from django import forms
# from django.core.files.base import File
# from django.db.models.base import Model
# from django.forms.utils import ErrorList
from django.forms import modelformset_factory,inlineformset_factory
from .models import Product,ProductAttachment

input_css_class="form-control"
# input_css_class="bg-gray-700 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'name', 'handle', 'price']
        # widgets = {
        #     'price_changed_stamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        # set style to single class
        # self.fields['name'].widget.attrs['placeold']="your name"
        # set to all class
        for field in self.fields:
            self.fields[field].widget.attrs['class']=input_css_class

    # def clean_price(self):
    #     price = self.cleaned_data.get('price')
    #     og_price = self.cleaned_data.get('og_price')

    #     if price <= 0:
    #         raise forms.ValidationError("The price must be a positive number.")

    #     if price > og_price:
    #         raise forms.ValidationError("The price cannot be higher than the original price.")
        
    #     return price

    # def clean_og_price(self):
    #     og_price = self.cleaned_data.get('og_price')
    #     if og_price <= 0:
    #         raise forms.ValidationError("The original price must be a positive number.")
    #     return og_price


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'handle', 'price']
 
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']=input_css_class

class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = ['file','name','is_free','active']
 
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            if field in ['is_free','active']:
                continue
            self.fields[field].widget.attrs['class']=input_css_class



ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    form=ProductAttachmentForm,
    fields=['file','name','is_free','active'],
    extra=0,
    can_delete=False
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    form=ProductAttachmentForm,
    formset=ProductAttachmentModelFormSet,
    fields=['file','name','is_free','active'],
    extra=0,
    can_delete=False
)