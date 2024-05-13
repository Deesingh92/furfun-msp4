
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'sku', 'name', 'description', 'price', 'rating', 'image', 'image_url', 'quantity']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['rating'].required = False
        self.fields['image_url'].required = False
        self.fields['quantity'].required = False
