from django.urls import path, include
from . import views

app_name = "auth"

urlpatterns = [
    path('register/', views.register_user, name='user_register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/',  views.MyTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.logout_user, name='user_logout'),
]  