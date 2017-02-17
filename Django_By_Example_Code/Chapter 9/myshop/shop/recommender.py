# -*- coding: utf-8 -*-
import redis
from django.conf import settings
from .models import Product


# 连接redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # 得到和这个商品一起购买的商品
                if product_id != with_id:
                    # 递增一起购买的商品的分数
                    r.zincrby(self.get_product_key(product_id),
                              with_id,
                              amount=1)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # 只有一件商品
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # 生成temporary key, join的用法
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # 多件商品,获得keys分数求和的集合
            # 保存结果集合到temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys) #Redis' ZUNIONSTORE用法,获得keys分数求和的集合
            # 删除输入的商品id
            r.zrem(tmp_key, *product_ids)
            # 得到推荐的商品id,递减排列
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # 删除temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions] #一件或多件商品

        # 得到推荐商品, objects.filter的用法
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id)) # lambda的用法, 按x.id排序
        return suggested_products

    def clear_purchases(self):
        #objects.values_list, delete的用法
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
