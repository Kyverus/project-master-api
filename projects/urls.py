from django.urls import path
from . import views

urlpatterns = [
    path('', views.projectsList),
    path('<str:pk>', views.projectObject),

]
