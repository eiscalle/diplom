from diplom.video.views import CategoryList, CategoryDetail
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
   url(r'^$', CategoryList.as_view(), name='category_list'),
   url(r'^category/(?P<pk>\d+)/$', CategoryDetail.as_view(), name='category_detail'),
   url(r'^video/(?P<pk>\d+)/$', CategoryDetail.as_view(), name='category_detail'),
)
