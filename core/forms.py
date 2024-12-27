from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Div, HTML
from crispy_forms.bootstrap import InlineField
from .models import Company, Department, Affiliate, Employee
from django.db.models import Q
import re

# Function to rename first choice in selection menu
def set_first_choice(field, placeholder):
    """Set the first choice of a specified field."""
    choices = list(field.choices)  # Convert to list
    choices[0] = ('', placeholder)  # Rename first choice with the provided placeholder
    field.choices = choices  # Set the modified choices

# Function to set attributes for all fields in the form
def set_field_attrs(form):
    """Set common attributes for all fields in the form."""
    for field_name in form.fields:
        field = form.fields.get(field_name)
        # Common attributes
        field.widget.attrs['placeholder'] = field.label  # Set placeholder as field label
        field.widget.attrs['dir'] = 'rtl'  # Set text direction
        field.widget.attrs['autocomplete'] = 'off'  # Disable autocomplete
        field.label = ''  # Clear the label


        # Set specific patterns based on field name
        if field_name == 'name' :
            # Allow Arabic letters only.
            field.widget.attrs['pattern'] = r'^[\u0621-\u064A\s]+$'

            def clean_name():
                name = form.cleaned_data['name']
                if not re.match(r'^[\u0621-\u064A\s]+$', name):
                    raise forms.ValidationError('الرجاء إستخدام الحروف العربية.')
                return name
            form.clean_name = clean_name

        elif field_name == 'phone':
            # Allow digits only.
            field.widget.attrs['pattern'] = r'^\d+$'

            def clean_phone():
                phone = form.cleaned_data['phone']
                if not re.match(r'^09\d{8}$', phone):
                    raise forms.ValidationError('يرجى إدخال رقم هاتف صحيح ابتداء بـ09.')

                return phone
            form.clean_phone = clean_phone

        elif 'date' in field_name:
            # Add Flatpickr attributes for date fields
            field.widget.attrs['id'] = 'monthSelector'  # Class for Flatpickr


# Entity Forms
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
        set_field_attrs(self)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['type', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_first_choice(self.fields['type'], 'نوع التقسيم')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('type', css_class='form-control'), css_class='col-sm-2'),  # Small column for type
                Div(Field('name', css_class='form-control'), css_class='col-sm-10'),  # Wider column for name
                css_class='input-group mb-2'  # Bootstrap class for a row
            ),
            Submit('submit', '{% if form.instance.id %}تحديث{% else %}اضافة{% endif %}', css_class='btn btn-primary')
        )
        set_field_attrs(self)


class AffiliateForm(forms.ModelForm):
    class Meta:
        model = Affiliate
        fields = ['type', 'name', 'subtype', 'subname', 'address']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_first_choice(self.fields['type'], 'نوع الجهة')
        set_first_choice(self.fields['subtype'], 'التقسيم الاداري')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('type', css_class='form-control'), css_class='col-sm-2'),  # Small column for type
                Div(Field('name', css_class='form-control'), css_class='col-sm-10'),  # Wider column for name
                css_class='input-group mb-2'  # Bootstrap class for a row
            ),
            Div(
                Div(Field('subtype', css_class='form-control'), css_class='col-sm-2'),  # Small column for type
                Div(Field('subname', css_class='form-control'), css_class='col-sm-10'),  # Wider column for name
                css_class='input-group mb-2'  # Bootstrap class for a row
            ),
            Field('address', css_class='form-control'),
            Submit('submit', '{% if form.instance.id %}تحديث{% else %}اضافة{% endif %}', css_class='btn btn-primary')
        )
        set_field_attrs(self)


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'job_title', 'department', 'email', 'phone', 'date_employed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_first_choice(self.fields['job_title'], 'الوظيفة')
        set_first_choice(self.fields['department'], 'الادارة/المكتب')
        # Filter the queryset for the department field
        self.fields['department'].queryset = Department.objects.filter(Q(type='Department') | Q(type='Office'))
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Div(
                Div(Field('job_title', css_class='form-control'), css_class='col-sm-4'),  # Small column for type
                Div(Field('department', css_class='form-control'), css_class='col-sm-8'),  # Wider column for name
                css_class='input-group mb-1'  # Bootstrap class for a row
            ),
            Div(
                Div(Field('email', css_class='form-control'), css_class='col-sm-4'),  # Small column for type
                Div(Field('phone', css_class='form-control'), css_class='col-sm-4'),  # Wider column for name
                Div(Field('date_employed', css_class='form-control'), css_class='col-sm-4'),  # Wider column for name
                css_class='input-group mb-1'  # Bootstrap class for a row
            ),
            Submit('submit', '{% if form.instance.id %}تحديث{% else %}اضافة{% endif %}', css_class='btn btn-primary')
        )
        set_field_attrs(self)

