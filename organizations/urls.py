from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.organizationList, name="organization_list"),
    path('<str:pk>', views.organizationObject, name="organization_object" ),
    path('<str:orgpk>/members/', include("memberships.urls")),
    path('<str:orgpk>/applications/', include("applications.urls")),
]
