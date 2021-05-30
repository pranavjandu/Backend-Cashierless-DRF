from django.conf.urls import include, url
from django.urls import path, include
from rest_framework import routers
from django.contrib import admin
from apps.users import views

admin.autodiscover()
router = routers.DefaultRouter()

urlpatterns = [
    path('api/',views.CustomerListView.as_view(),name='customer_list'),
    path('api/<int:id>/',views.CustomerDetailView.as_view(),name='customer_detail')
]