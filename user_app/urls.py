from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from gear_app.views import gear_dashboard

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user_app/logout.html'), name='logout'),
    path('user/', views.dashboard_view, name='user'),
    path('gear_app/gear_dashboard', gear_dashboard, name='gear_dashboard')
]