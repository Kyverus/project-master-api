from django.urls import path
from . import views

urlpatterns = [
    path("", views.organizationMembers, name="member_list"),
    path('<str:memberpk>', views.memberObject, name="member_object" ),
    path('<str:memberpk>/admin-add', views.administratorStatusAddition, name="add_admin_status" ),
    path('<str:memberpk>/admin-remove', views.administratorStatusRemoval, name="remove_admin_status" ),
]
