from django.conf.urls import url

from . import views

app_name = 'cooks'

urlpatterns = [
    url(r'^$', views.cook_list, name='list'),
    url(r'^like/$', views.like, name='like'),
    url(r'^favorite/$', views.favorite, name='favorite'),
    url(r'^(?P<recipe_slug>.+)/$', views.cook_detail, name='detail'),
    url(r'^(?P<recipe_slug>.+)/edit', views.edit_recipe, name='edit_recipe'),
]
