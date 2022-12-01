from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('lclinfo', views.lclinfo, name='lclinfo'),
    path('lcladd', views.lcladd, name='lcladd'),
    path('lcldelete', views.lcldelete, name='lcldelete'),
    path('lclupdate', views.lclupdate, name='lclupdate'),
    path('quotation', views.quotation, name='quotation'),
    path('showquote', views.showquote, name='showquote'),
    path('airinfo', views.airinfo, name='airinfo'),
    path('airadd', views.airadd, name='airadd'),
    path('airupdate', views.airupdate, name='airupdate'),
    path('airdelete', views.airdelete, name='airdelete'),
    path('fclinfo', views.fclinfo, name='fclinfo'),
    path('fcladd', views.fcladd, name='fcladd'),
    path('fclupdate', views.fclupdate, name='fclupdate'),
    path('fcldelete', views.fcldelete, name='fcldelete'),
    path('airotherinfo', views.airotherinfo, name='airotherinfo'),
    path('airotheradd', views.airotheradd, name='airotheradd'),
    path('airotherdelete', views.airotherdelete, name='airotherdelete'),
    path('airotherupdate', views.airotherupdate, name='airotherupdate'),
    
]
