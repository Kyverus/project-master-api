from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path('', views.projectList, name="project_list"),
    path('<str:pk>', views.projectObject, name="project_object"),

]
