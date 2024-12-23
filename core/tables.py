import django_tables2 as tables
from .models import Company, Department, Affiliate, Employee

class CompanyTable(tables.Table):
    class Meta:
        model = Company
        template_name = "django_tables2/bootstrap.html"  # or any other template you want to use
        fields = ("name", "address", "phone")

class DepartmentTable(tables.Table):
    class Meta:
        model = Department
        template_name = "django_tables2/bootstrap.html"
        fields = ("type", "name")

class AffiliateTable(tables.Table):
    class Meta:
        model = Affiliate
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "association")

class EmployeeTable(tables.Table):
    class Meta:
        model = Employee
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "job_title", "email", "phone", "date_employed")