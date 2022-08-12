from django.urls import path

from . import views

urlpatterns = [  
    # TODO: make webhook more secure
    path('', views.index, name="index"),

]