#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import models

CART_ID = 'CART-ID'


class ItemDoesNotExist(Exception):
    pass


class Cart:
    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            item.quantity += 1
            item.save()

    def remove(self, item):
        try:
            item = models.Item.objects.get(pk=item.pk)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def checkout(self):
        self.cart.checked_out = True
        self.cart.save()
        return True
