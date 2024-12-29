import django_tables2 as tables
from .models import AssetCategory, Asset, ImportRecord
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
    edit = tables.Column(accessor='id', verbose_name='Action', empty_values=())

    class Meta:
        model = Asset
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'category', 'brand', 'brand_en', 'unit')

    def render_edit(self, value, record):
        return mark_safe(f'<a href="{reverse("manage_assets")}?category={record.category.id}&id={value}" class="btn btn-secondary">تعديل</a>')


class ImportRecordTable(tables.Table):
    details = tables.Column(accessor='trans_id', verbose_name='*', empty_values=())

    # Define table columns
    trans_id = tables.Column()
    company = tables.Column()
    date = tables.Column()

    class Meta:
        model = ImportRecord
        template_name = "django_tables2/bootstrap5.html"  # You can choose a different template style
        fields = ("trans_id", "date", "assign_number", "assign_date", "items", "company")  # Fields to display in the table

    def render_details(self, value):
        return mark_safe(f'<a href="{reverse("import_details", args=[value])}" class="btn btn-secondary">عرض</a>')
