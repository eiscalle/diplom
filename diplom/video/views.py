# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from diplom.video.models import Category
from django.views.generic import ListView, DetailView


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['videos'] = self.object.videos.filter(is_moderated=True)
        return context


class VideoyDetail(DetailView):
    model = Category
    template_name = 'video_detail.html'