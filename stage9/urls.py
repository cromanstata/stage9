"""stage9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.views.generic.base import TemplateView
from . import views
from . import settings
import allauth.account.views

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^recipes/', include('cooks.urls')),
    url(r'^friendship/', include('friendship.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^profile/(?P<name>[\w.@+-]+)/$', views.profile, name='user'),
    url(r'^profile/(?P<name>[\w.@+-]+)/update/$', views.edit_user, name='update'),
    url(r'^profile/(?P<name>[\w.@+-]+)/favs/$', views.favorites, name='favs'),
    url(r'^profile/(?P<name>[\w.@+-]+)/post/$', views.add_recipe, name='add_recipe'),
    url(r'^profile/(?P<name>[\w.@+-]+)/recipes/$', views.my_recipes, name='my_recipes'),
    #url(r'^profile/(?P<name>[\w.@+-]+)/recipes/(?P<recipe>[\w.@+-]+)/edit/$', views.edit_recipe, name='edit_recipe'),
    url(r'^search/$', views.search, name='search'),
    url(r'^allauthpop/$', views.allauthpop, name='allauthpop'),
    url(r'^tags/$', views.get_tags, name='tags'),
    url(r'^titles/$', views.get_titles, name='titles'),
    url(r'^diff_tags/$', views.get_diff_tags, name='diff_tags'),
    url(r'^availble_tags/$', views.availble_tags, name='availble_tags'),
    url(r'^follow/$', views.follow, name='follow'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#(?P<nameid>[0-9]+)