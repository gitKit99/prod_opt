from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),
    path('create', views.create, name='create'),
    path('calculate', views.calculate, name='calculate'),
    path('result', views.result, name='result'),
    path('save_result', views.save_result, name='save_result'),
]
