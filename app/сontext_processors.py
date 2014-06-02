# -*- coding: utf-8 -*-
from diplom.video.models import Category


def cat_list(request):
    return {'ALL_CATS': Category.objects.all()}