from django.urls import path
from . import views

urlpatterns = [
    path('', views.organizationList, name="organization_list"),
    # path('<str:pk>', views.organizationObject, name="organization_object" )
]
