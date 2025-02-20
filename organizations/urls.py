from django.urls import path, include
from . import views

app_name = "organizations"

urlpatterns = [
    path('', views.organizationList, name="organization_list"),
    path('<str:pk>', views.organizationObject, name="organization_object" ),
    path('<str:orgpk>/members/', views.organizationMembers, name="organization_members"),
    path('<str:orgpk>/applications/', views.organizationApplications, name="organization_applications"),
]
