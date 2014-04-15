# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect


def login_required(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return wrapper


def require_http_methods(view, request_method_list):
    def wrapper(request, *args, **kwargs):
        if request.method in request_method_list:
            return view(request, *args, **kwargs)
        else:
            return JSONResponseMixin().render_to_response(error='Method not allowed')
    return wrapper


def require_safe(view):
    return require_http_methods(view, ['GET', 'HEAD'])


def require_get(view):
    return require_http_methods(view, ['GET'])


def require_post(view):
    return require_http_methods(view, ['POST'])