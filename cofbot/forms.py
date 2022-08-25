from dataclasses import field
from urllib.request import OpenerDirector
from django.forms.models import inlineformset_factory
from django import forms
from .models import *

class BroadcastForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('Product', 'Count')

class BuyingForm(forms.ModelForm):
    class Meta:
        model = Buying
        fields = ['Customer']

    widgets = {
            # 'author': forms.TextInput(attrs={'class': 'form-control'}),
            'Customer': forms.Select(attrs={'class': 'form-control', 'name': 'fields', 'hx-get':"{% url 'create-buy-customer' %}", 'hx-trigger':'change', 'hx-target':'Wells'}),
            # 'Barista': forms.Select(attrs={'class': 'form-control'}),
        }


