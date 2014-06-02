# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from diplom.video.forms import VideoForm
from diplom.video.models import Category, Video, Subtitle
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView
from pytils.translit import translify


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


class VideoDetail(DetailView):
    model = Video
    template_name = 'video_detail.html'


class VideoCreate(CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'video_create.html'
    errors = []
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.errors = []
        self.ru_sub = self.request.FILES.get('ru_sub')
        self.en_sub = self.request.FILES.get('en_sub')
        if not self.ru_sub:
            self.errors.append('Русские субтитры: Обязательное поле.')
        if not self.en_sub:
            self.errors.append('Английские субтитры: Обязательное поле.')

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid() and not self.errors:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        if self.errors is None:
            self.errors = []
        for key, error in form.errors.items():
            self.errors.append(form.fields[key].label + ': ' + error[0])

        return super(VideoCreate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(VideoCreate, self).get_context_data(**kwargs)
        context['errors'] = self.errors
        return context

    def form_valid(self, form):

        source = self.request.FILES.get('source')
        poster = self.request.FILES.get('poster')
        form.instance.source = default_storage.save(translify(source.name), ContentFile(source.read()))
        form.instance.poster = default_storage.save(translify(poster.name), ContentFile(poster.read()))
        form.instance.user = self.request.user

        self.object = form.save()

        subtitle = Subtitle()
        subtitle.lang = 'ru'
        subtitle.video = self.object
        subtitle.source = default_storage.save(translify(self.ru_sub.name), ContentFile(self.ru_sub.read()))
        subtitle.save()
        subtitle.pk = None
        subtitle.source = default_storage.save(translify(self.en_sub.name), ContentFile(self.en_sub.read()))
        subtitle.lang = 'en'
        subtitle.save()



        return HttpResponseRedirect(self.get_success_url())

