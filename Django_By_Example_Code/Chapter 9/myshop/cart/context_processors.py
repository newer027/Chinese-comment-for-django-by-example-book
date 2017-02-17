# -*- coding: utf-8 -*-
from .cart import Cart

def cart(request):
    return {'cart': Cart(request) } #request的用法
