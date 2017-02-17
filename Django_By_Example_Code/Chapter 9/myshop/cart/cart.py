# -*- coding: utf-8 -*-
from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):

    def __init__(self, request):
        """
        初始化购物车
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 保存空购物车到会话
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # 保存当前优惠券
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        """
        对商品计数
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        遍历购物车中商品,从数据库取得商品
        """
        product_ids = self.cart.keys()
        # 获取商品对象,添加到购物车
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        """
        添加商品到购物车,更新数量
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        删除购物车中的商品
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # 更新会话中购物车
        self.session[settings.CART_SESSION_ID] = self.cart
        # 标记会话已经修改,保证会话已经保存
        self.session.modified = True

    def clear(self):
        # 空的购物车
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_total_price(self):
        #sum, Decimal的用法
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_discount(self):
        if self.coupon:
            #Decimal的用法
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0') #如果没有优惠券

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount() #总价-折扣价
