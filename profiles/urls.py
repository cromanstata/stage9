from django.conf.urls import url

from . import views

app_name = 'profiles'

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^update/', views.edit_user, name='account_update'),
    url(r'^faves/', views.favorites, name='favs'),
    url(r'^add_recipe/', views.add_recipe, name='add_recipe'),
    url(r'^my_recipes/', views.my_recipes, name='my_recipes'),
#    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
#    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]