# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon')) #gettext_lazy的用法
