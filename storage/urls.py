from django.urls import path
from . import views
from core import views as users
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('storage/assets/', views.manage_assets, name='manage_assets'),
    # path('storage/assets/<str:category>/', views.manage_assets, name='manage_assets'),
    path('storage/categories/', views.manage_category, name='manage_category'),
    path('storage/categories/<int:category_id>/', views.manage_category, name='edit_category'),
    path('storage/import/', views.import_records, name='import_records'),
    path('storage/import/new/', views.import_create, name='import_create'),
    path("storage/import/new/add/", views.import_item_add, name="import_item_add"),
    path('storage/import/new/<int:asset_id>/', views.import_item_delete, name='import_item_delete'),
    path('storage/import/new/cancel', views.import_cancel, name='import_cancel'),
    # path('storage/import/edit/<int:trans_id>/', views.import_record_edit, name='import_item_edit'),
    # path('storage/import/record/delete/<int:trans_id>/', views.import_record_delete, name='import_record_delete'),

]