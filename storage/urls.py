from django.urls import path
from . import views
from core import views as users
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('storage/assets/', views.manage_assets, name='asset_management'),
    path('storage/assets/<str:category>/', views.manage_assets, name='asset_management'),
    path('storage/categories/', views.manage_categories, name='manage_categories'),
    path('storage/categories/<int:category_id>/', views.manage_categories, name='edit_category'),

]