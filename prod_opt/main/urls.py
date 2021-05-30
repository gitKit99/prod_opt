from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('add', views.add, name='add'),
    path('comp', views.comp, name='comp'),
    path('add_in', views.add_in, name='add_in'),
    path('about', views.create, name='about'),
    path('calculate', views.calculate, name='calculate'),
    path('result', views.result, name='result'),
    path('save_result', views.save_result, name='save_result'),
]
