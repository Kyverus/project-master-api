from django.urls import path
from . import views

app_name = "memberships"

urlpatterns = [
    path("", views.membershipList, name="membership_list"),
    path('<str:membershippk>', views.membershipObject, name="membership_object" ),
    path('<str:membershippk>/admin-add', views.administratorStatusAddition, name="add_admin_status" ),
    path('<str:membershippk>/admin-remove', views.administratorStatusRemoval, name="remove_admin_status" ),
]
