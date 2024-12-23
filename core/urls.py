from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Index Url
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('clear_login_modal_flag/', views.clear_login_modal_flag, name='clear_login_modal_flag'),
    path('manage/<str:model_name>/', views.manage_sections, name='manage_sections'),
]