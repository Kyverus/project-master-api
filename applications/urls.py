from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("", views.applicationList, name="application_list"),
    path('<str:applicationpk>', views.applicationObject, name="application_object" ),
    path('<str:applicationpk>/accept', views.acceptApplication, name="application_accept" ),
    path('<str:applicationpk>/reject', views.rejectApplication, name="application_reject" ),
]
