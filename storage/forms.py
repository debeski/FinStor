from django import forms
from django.contrib.contenttypes.models import ContentType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import Department, Affiliate, Employee, Asset, ImportRecord, ImportItem, ExportRecord, ExportItem 



# New Asset Form
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['type', 'name', 'brand', 'unit', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'type',
            'name',
            'brand',
            'unit',
            'quantity',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )


# New ImportRecord Form
class ImportRecordForm(forms.ModelForm):
    class Meta:
        model = ImportRecord
        fields = ['company', 'date', 'assign_number', 'assign_date', 'notes', 'pdf_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'company',
            'date',
            'assign_number',
            'assign_date',
            'notes',
            'pdf_file',
            Submit('submit', 'Save and Print', css_class='btn btn-primary')
        )

# New ImportItem Form
class ImportItemForm(forms.ModelForm):
    class Meta:
        model = ImportItem
        fields = ['trans_id', 'asset', 'quantity', 'return_at', 'return_purpose', 'return_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'trans_id',
            'asset',
            'quantity',
            'return_at',
            'return_purpose',
            'return_notes',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )

# New Return ImportItem Form
class ReturnFromStorageForm(forms.ModelForm):
    class Meta:
        model = ImportItem
        fields = ['asset', 'quantity', 'return_at', 'return_purpose', 'return_condition', 'return_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('asset'),
            Field('quantity'),
            Field('return_at'),
            Field('return_purpose'),
            Field('return_notes'),
            Submit('submit', 'Save')
        )


# New ExportRecord Form
class ExportRecordForm(forms.ModelForm):
    class Meta:
        model = ExportRecord
        fields = ['export_type', 'entity_selection', 'date', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save & Print'))
        
        # Dynamically update the entity_selection choices based on export_type
        export_type = self.initial.get('export_type')
        
        if export_type == 'Personal':
            # Populate with Employee Name
            self.fields['entity_selection'].queryset = Employee.objects.all()
        elif export_type == 'Department':
            # Populate with Department Name
            self.fields['entity_selection'].queryset = Department.objects.all()
        elif export_type == 'Loan':
            # Populate with Affiliate Name
            self.fields['entity_selection'].queryset = Affiliate.objects.all() | Affiliate.objects.all()
        else:
            # For 'Consume' Populate with Department Name
            self.fields['entity_selection'].queryset = Department.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        export_type = cleaned_data.get('export_type')
        entity_selection = cleaned_data.get('entity_selection')

        # Add additional validations if needed, for example:
        if export_type == 'Personal' and not isinstance(entity_selection, Employee):
            raise forms.ValidationError("For 'Personal' export type, select an Employee.")
        if export_type == 'Department' and not isinstance(entity_selection, Department):
            raise forms.ValidationError("For 'Department' export type, select a Department.")
        if export_type == 'Loan' and not isinstance(entity_selection, Affiliate):
            raise forms.ValidationError("For 'Loan' export type, select an Affiliate.")
        if export_type == 'Consume' and not isinstance(entity_selection, Department):
            raise forms.ValidationError("For 'Consume' export type, select a Department.")
        
        return cleaned_data

# New ExportItem Form
class ExportItemForm(forms.ModelForm):
    class Meta:
        model = ExportItem
        fields = ['trans_id', 'asset', 'quantity', 'sn', 'pic', 'return_at', 'return_purpose', 'return_condition', 'return_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'trans_id',
            'asset',
            'quantity',
            'sn',
            'pic',
            'return_at',
            'return_purpose',
            'return_condition',
            'return_notes',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )

# New Return ExportItem Form
class ReturnToStorageForm(forms.ModelForm):
    class Meta:
        model = ExportItem
        fields = ['asset', 'quantity', 'sn', 'pic', 'return_at', 'return_purpose', 'return_condition', 'return_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('asset'),
            Field('quantity'),
            Field('sn'),
            Field('pic'),
            Field('return_at'),
            Field('return_purpose'),
            Field('return_condition'),
            Field('return_notes'),
            Submit('submit', 'Save')
        )

