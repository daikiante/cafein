from django.urls import path
from . import views
from .views import EditProfile
from django.contrib.auth import views as auth_views


app_name = 'user'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'),name='login'),
    path('logout/', views.logout_func, name='logout'),
    path('edit/<int:pk>', EditProfile.as_view(), name='edit'),
]