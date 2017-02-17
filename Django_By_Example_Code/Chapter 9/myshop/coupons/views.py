# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST) #request.POST的用法
    if form.is_valid():
        code = form.cleaned_data['code'] #cleaned_data的用法
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                    valid_from__lte=now,
                                    valid_to__gte=now,
                                    active=True) #objects.get的用法
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None #DoesNotExist,None的用法
    return redirect('cart:cart_detail') #redirect的用法
