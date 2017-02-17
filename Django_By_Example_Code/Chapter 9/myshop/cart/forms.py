# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)] #str, range的用法


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,
                                      label=_('Quantity')) #TypedChoiceField,choices的用法
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput) #forms.HiddenInput的用法
