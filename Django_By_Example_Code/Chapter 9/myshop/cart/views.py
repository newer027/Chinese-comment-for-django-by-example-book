# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender


@require_POST #装饰器的用法
def cart_add(request, product_id):
    cart = Cart(request) #request的用法
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST) #request.POST的用法
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update']) #cart.add的用法
    return redirect('cart:cart_detail') #redirect的用法


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product) #分别获取cart,product,然后执行remove
    return redirect('cart:cart_detail') #redirect的用法


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True}) #update_quantity_form=>item=>cart传递到detail.html
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart] #item['product']的用法
    recommended_products = r.suggest_products_for(cart_products, max_results=4) #Recommender的用法

    return render(request, 'cart/detail.html', {'cart': cart,
                                                'coupon_apply_form': coupon_apply_form,
                                                'recommended_products': recommended_products}) #render的用法
