"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from mywebsite import views as core_views
from charity import views as charity_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

urlpatterns = [
    url(r'^$', core_views.index),
    url(r'^login/$', core_views.login_route, name='login'),
    url(r'^logout/$', core_views.logout_route, name='logout'),
    url(r'^signup/$', charity_views.signup, name='signup'),
    url(r'^charities/$', charity_views.charities),
    # ^ change core_views to charity_views bc we are changing the pattern
    path('charity/<charity_name>/<charity_id>/', charity_views.charity),
    path('charity/<charity_name>/<charity_id>/update/', charity_views.charity_update),
    url(r'^charity/create/$', charity_views.signup_submit),
    path('campaign/<campaign_id>/add/', charity_views.add_campaign_item),
    path('campaign-item/<campaign_item_id>/delete/', charity_views.delete_campaign_item),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
