import django_tables2 as tables
from .models import AssetCategory, Asset
from django.utils.safestring import mark_safe
from django.urls import reverse


class AssetCategoryTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='Action', empty_values=())

    class Meta:
        model = AssetCategory
        template_name = "django_tables2/bootstrap5.html"
        fields = ['name', 'discription']
        attrs = {'class': 'table table-striped'}

    def render_edit(self, value):
        return mark_safe(f'<a href="{reverse("edit_category", args=[value])}" class="btn btn-secondary">تعديل</a>')

class AssetTable(tables.Table):
    class Meta:
        model = Asset
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'category', 'brand', 'unit')
