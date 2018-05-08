from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
   #url(r'^introspect/(?P<pk>[0-9]+)/$', views.IntrospectList.as_view()),    
]
