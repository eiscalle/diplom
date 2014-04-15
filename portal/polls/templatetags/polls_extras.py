#-*- coding: utf-8 -*-
from django import template

register = template.Library()

def get_item(item, key):
    if isinstance(item, list):
        return item[int(key)]
    return item.get(int(key))


register.filter('get_item', get_item)
