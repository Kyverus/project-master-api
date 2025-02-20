from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('auth/', include('auth.urls')),
    path('projects/', include('projects.urls')),
    path('organizations/', include('organizations.urls')),
    path('memberships/', include('memberships.urls')),
    path('applications/', include('applications.urls')),
]
