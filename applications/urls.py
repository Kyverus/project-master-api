from django.urls import path
from . import views


urlpatterns = [
    path("", views.organizationApplications, name="application_list"),
    path('<str:applicationpk>', views.applicationObject, name="application_object" ),
    path('<str:applicationpk>/accept', views.acceptApplication, name="application_accept" ),
    path('<str:applicationpk>/reject', views.rejectApplication, name="application_reject" ),
]
