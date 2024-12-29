from django import forms
from django.contrib.contenttypes.models import ContentType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from crispy_forms.bootstrap import FormActions
from .models import Company, Department, Affiliate, Employee, AssetCategory, Asset, ImportRecord, ImportItem, ExportRecord, ExportItem 
from core.forms import set_field_attrs, set_first_choice
from django.urls import reverse



class AssetCategoryForm(forms.ModelForm):
    class Meta:
        model = AssetCategory
        fields = ['name', 'discription']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        # Define the cancel button HTML only if the instance has an ID
        cancel_button = ""
        if self.instance.id:
            cancel_button = '<a href="#" onclick="window.history.back();" class="btn btn-danger">إلغاء</a>'


        self.helper.layout = Layout(
            Div(
                Div(Field('name', css_class='form-control'), css_class='col-sm-5'),
                Div(Field('discription', css_class='form-control'), css_class='col-sm-7'),
                css_class='input-group mb-1'
            ),
            FormActions(
                Submit('submit', '{% if form.instance.id %}تحديث{% else %}اضافة{% endif %}', css_class='btn btn-primary'),
                HTML(cancel_button)  # Cancel button is shown conditionally
            )
        )
        set_field_attrs(self)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if AssetCategory.objects.filter(name=name).exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name
    
    
# New Asset Form
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['category', 'name', 'brand', 'brand_en', 'unit']

    def __init__(self, *args, **kwargs):
        self.selected_cat = kwargs.pop('selected_cat', None)
        super().__init__(*args, **kwargs)
        set_first_choice(self.fields['category'], 'التصنيف')

        # Dynamically set the type field
        if self.selected_cat:
            self.fields['category'].initial = self.selected_cat
            self.fields['category'].widget = forms.HiddenInput()

        # Configure crispy form helper
        self.helper = FormHelper()

        # Define the cancel button HTML only if the instance has an ID
        cancel_button = ""
        if self.instance.id:
            cancel_button = '<a href="#" onclick="window.history.back();" class="btn btn-danger">إلغاء</a>'

        self.helper.layout = Layout(
            'category',
            Div(
                Div(Field('name', css_class='form-control'), css_class='col-sm-4'),
                Div(Field('brand', css_class='form-control'), css_class='col-sm-3'),
                Div(Field('brand_en', css_class='form-control'), css_class='col-sm-3'),
                Div(Field('unit', css_class='form-control'), css_class='col-sm-2'),
                css_class='input-group mb-1'
            ),
            FormActions(
                Submit('submit', '{% if form.instance.id %}تحديث{% else %}اضافة{% endif %}', css_class='btn btn-primary'),
                HTML(cancel_button)  # Cancel button is shown conditionally
            )
        )
        set_field_attrs(self)


# New ImportRecord Form
class ImportRecordForm(forms.ModelForm):
    class Meta:
        model = ImportRecord
        fields = ['company', 'date', 'assign_number', 'assign_date', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.all()
        self.fields['notes'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('company', css_class='form-control'), css_class='col-sm-8'),
                Div(Field('date', css_class='form-control'), css_class='col-sm-4'),
                css_class='input-group mb-1'
            ),
            Div(
                Div(Field('assign_number', css_class='form-control'), css_class='col-sm-6'),
                Div(Field('assign_date', css_class='form-control'), css_class='col-sm-6'),
                css_class='input-group mb-1'
            ),
            Field('notes', css_class='form-control', rows=1),
            FormActions(
                Submit('submit_record', 'حفظ اذن الاستلام', css_class='btn btn-primary'),
                HTML('<a href="{% url \'import_cancel\' %}" class="btn btn-danger">الغاء</a>'),
            )
        )
        set_field_attrs(self)

class ImportItemForm(forms.ModelForm):

    asset_cat = forms.ModelChoiceField(
    queryset=AssetCategory.objects.all(),
    required=False,
    label="اختر التصنيف"
)
    class Meta:
        model = ImportItem
        fields = ['asset_cat', 'asset', 'price', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.all()
        self.fields['asset'].required = False
        self.fields['price'].required = False
        self.fields['quantity'].required = False
        self.fields['quantity'].widget.attrs.update({
            'min': '1.00',
        })
        self.fields['price'].widget.attrs.update({
            'min': '1.00',
            'step': '1.00',
            'value': '1.00',
        })
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('asset_cat', css_class='form-control', id='id_asset_cat'),
            Field('asset', css_class='form-control', id='id_asset'),
            Div(
                Div(Field('quantity', css_class='form-control'), css_class='col-sm-6'),
                Div(Field('price', css_class='form-control'), css_class='col-sm-6'),
                css_class='input-group mb-1'
            ),
            FormActions(
                Submit('submit', 'اضافة صنف', css_class='btn btn-primary'),
            )
        )
        set_field_attrs(self)

# New Return ImportItem Form
class ReturnFromStorageForm(forms.ModelForm):
    class Meta:
        model = ImportItem
        fields = ['asset', 'quantity', 'return_at', 'return_purpose', 'return_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('asset', placeholder='Select Asset', label=''),
            Field('quantity', placeholder='Enter Quantity', label=''),
            Field('return_at', placeholder='Return Date', label=''),
            Field('return_purpose', placeholder='Purpose of Return', label=''),
            Field('return_notes', placeholder='Additional Notes', label='', css_class='form-control', rows=3),
            Submit('submit', 'Save', css_class='btn btn-primary')
        )


# New ExportRecord Form
class ExportRecordForm(forms.ModelForm):
    class Meta:
        model = ExportRecord
        fields = ['trans_id', 'export_type', 'date', 'notes']

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
            self.fields['entity_selection'].queryset = Affiliate.objects.all()
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
        fields = ['trans_id', 'asset', 'quantity', 'sn', 'pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'trans_id',
            'asset',
            'quantity',
            'sn',
            'pic',
            Submit('submit', 'Save', css_class='btn btn-primary')
        )

# New Return ExportItem Form
class ReturnToStorageForm(forms.ModelForm):
    class Meta:
        model = ExportItem
        fields = ['trans_id', 'asset', 'quantity', 'sn', 'pic', 'return_at', 'return_purpose', 'return_condition', 'return_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('trans_id'),
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

