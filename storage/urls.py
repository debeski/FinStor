from django.urls import path
from . import views
from core import views as users
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Index Url
    path('', views.index, name='index'),
    path('login/', users.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('clear_login_modal_flag/', users.clear_login_modal_flag, name='clear_login_modal_flag'),
]