from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.utils import timezone
from .forms import CompanyForm, DepartmentForm, AffiliateForm, EmployeeForm
from .models import Company, Department, Affiliate, Employee
from .tables import CompanyTable, DepartmentTable, AffiliateTable, EmployeeTable
from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.contrib.auth import authenticate, login
# from django.contrib import messages


logger = logging.getLogger('FinStor')


# Logger initiation Function:
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)


# Function to gather Core Model, Form, Table Classes and Arabic Names based on the model_name
def get_core_models(model_name=None):

    model_mapping = {
        'company': Company,
        'department': Department,
        'affiliate': Affiliate,
        'employee': Employee,
    }

    form_mapping = {
        'company': CompanyForm,
        'department': DepartmentForm,
        'affiliate': AffiliateForm,
        'employee': EmployeeForm,
    }

    table_mapping = {
        'company': CompanyTable,
        'department': DepartmentTable,
        'affiliate': AffiliateTable,
        'employee': EmployeeTable,
    }

    if model_name:
        model_class = model_mapping.get(model_name.lower())
        form_class = form_mapping.get(model_name.lower())
        table_class = table_mapping.get(model_name.lower())
        if not model_class:
        # Return None if model_name is not recognized
            return None, None
    else:
        # Return all models and forms if model_name is not provided
        return list(model_mapping.values()), None
    
    ar_name = model_class._meta.verbose_name
    ar_names = model_class._meta.verbose_name_plural

    return model_class, form_class, table_class, ar_name, ar_names


# Index view
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'base.html')
    

# Manage sections view
@login_required
def manage_sections(request, model_name):
    model_class, form_class, table_class, ar_name, ar_names = get_core_models(model_name)

    # Validate the model_class
    if not model_class or not form_class or not table_class:
        return render(request, 'manage_sections.html', {
            'model_name': model_name,
            'error': 'هناك خطأ في اسم المودل.',
        })

    # Handle document editing
    document_id = request.GET.get('id')
    instance = None
    if document_id:
        instance = get_object_or_404(model_class, id=document_id)

    form = form_class(request.POST or None, instance=instance)
    edited = True if document_id else False

    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('manage_sections', model_name=model_name)

    # Fetch objects and create the table
    objects = model_class.objects.all()
    table = table_class(objects, model_name=model_name)  # Ensure model_name is passed here

    # Handle sorting if applicable
    if model_name == model_name and 'sort' in request.GET:
        sort_field = request.GET['sort']
        objects = objects.order_by(sort_field)

    return render(request, 'manage_sections.html', {
        'model_name': model_name,
        'form': form,
        'table': table,
        'edited': edited,
        'ar_name': ar_name,
        'ar_names': ar_names,
    })



# def clear_login_modal_flag(request):
#     """ Clear the session flag to prevent the modal from showing again. """
#     if request.method == 'POST':  # We expect a POST request to clear the session flag
#         if 'show_login_modal' in request.session:
#             del request.session['show_login_modal']
#         return JsonResponse({'message': 'Login modal flag cleared'})
#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=405)
