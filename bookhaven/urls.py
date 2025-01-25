"""
URL configuration for bookhaven project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from bookhaven import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage),
    path('booksinfo',views.booksinfo),
    path('publisherinfo',views.publishersinfo),
    path('warehouseinfo',views.warehouseinfo),
    path('adminlogin',views.adminlogin),
    path('admindashboard',views.admindashboard),
    path('addbook',views.add_book),
    path('addpublisher',views.add_publisher),
    path('addauthor',views.add_author),
    path('addwarehouse',views.add_warehouse),
    path('deletebook',views.delete_book),
    path('deleteauthor',views.delete_author),
    path('deletepublisher',views.delete_publisher),
    path('deletewarehouse',views.delete_warehouse),
]
