from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ontology'),
    path('attributes', views.attributes, name='attributes'),
    path('requests', views.requests, name='requests'),
    path('relations', views.relations, name='relations'),
]