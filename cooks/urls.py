from django.conf.urls import url

from . import views

app_name = 'cooks'

urlpatterns = [
    url(r'^$', views.cook_list, name='list'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.cook_detail, name='detail'),
]
