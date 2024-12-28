from django.contrib import admin
from .models import Asset, AssetCategory

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'discription')
    search_fields = ('name', 'discription')

# Admin Configuration for Asset
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'unit')
    list_filter = ('category',)
    search_fields = ('name', 'brand')
    ordering = ('category', 'name')