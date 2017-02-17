# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True) #objects.all, object.filter的用法
    if category_slug:
        category = get_object_or_404(Category,
                                     translations__language_code=request.LANGUAGE_CODE,
                                     translations__slug=category_slug) #get_object_or_404的用法
        products = products.filter(category=category) #category的商品
    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products}) #render的用法


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True) #get_object_or_404的用法


    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4) #[product]是一件或多件商品
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products}) #render的用法