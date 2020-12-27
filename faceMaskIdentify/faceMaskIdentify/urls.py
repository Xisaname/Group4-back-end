"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views, testdb

urlpatterns = [
    path('testdb/', testdb.testdb),
    path('hello/', views.hello),
    path('detect/', views.detect),
    url(r'^receive/', views.receive),
    url(r'^user_images/', views.user_images),
    url(r'^user_registered/', views.user_registered),
    url(r'^user_getin/', views.user_getin)
]
