from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import Company, Department, Affiliate, Employee


# New Company Form
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'phone']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'address',
            'phone',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )


# New Department Form
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['type', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'type',
            'name',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )


# New Affiliate Form
class AffiliateForm(forms.ModelForm):
    class Meta:
        model = Affiliate
        fields = ['name', 'association']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'association',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )


# New Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'job_title', 'email', 'phone', 'date_employed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'job_title',
            'email',
            'phone',
            'date_employed',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )

