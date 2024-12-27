import django_tables2 as tables
from .models import Company, Department, Affiliate, Employee
from django.urls import reverse
from django.utils.safestring import mark_safe
from babel.dates import format_date


# Entity Models
class CompanyTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='Action', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name

    class Meta:
        model = Company
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'phone', 'address', 'edit')

    def render_edit(self, value):
        return mark_safe(f'<a href="{reverse("manage_sections", args=[self.model_name])}?id={value}" class="btn btn-secondary">تعديل</a>')


class DepartmentTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='Action', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name

    class Meta:
        model = Department
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'type', 'edit')

    def render_edit(self, value):
        return mark_safe(f'<a href="{reverse("manage_sections", args=[self.model_name])}?id={value}" class="btn btn-secondary">تعديل</a>')


class AffiliateTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='Action', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        
    class Meta:
        model = Affiliate
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'type', 'subname', 'subtype', 'address', 'edit')
    
    def render_edit(self, value):
        return mark_safe(f'<a href="{reverse("manage_sections", args=[self.model_name])}?id={value}" class="btn btn-secondary">تعديل</a>')


class EmployeeTable(tables.Table):
    edit = tables.Column(accessor='id', verbose_name='Action', empty_values=())

    def __init__(self, *args, model_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name

    class Meta:
        model = Employee
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'job_title', 'department', 'email', 'phone', 'date_employed', 'edit')

    def render_edit(self, value):
        return mark_safe(f'<a href="{reverse("manage_sections", args=[self.model_name])}?id={value}" class="btn btn-secondary">تعديل</a>')
    
    # Format date in Arabic
    def render_date_employed(self, value):
        if value:
            return format_date(value, format='MMMM yyyy', locale='ar')
        return 'N/A'
