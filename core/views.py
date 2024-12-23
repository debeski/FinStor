from django.shortcuts import render, redirect
import logging
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CompanyForm, DepartmentForm, AffiliateForm, EmployeeForm
from .models import Company, Department, Affiliate, Employee
from .tables import CompanyTable, DepartmentTable, AffiliateTable, EmployeeTable


logger = logging.getLogger('FinStor')



# Logger initiation Function:
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)



def index(request):
    return render(request, 'base.html')



def user_login(request):
    user_name = None  # Initialize the variable to store the user's name

    # If the user is already authenticated, redirect to index
    if request.user.is_authenticated:
        if request.user.is_staff:  # Admin users (staff) shouldn't use the login modal
            logger.info(f"Admin {request.user.username} is already logged in.")
            return redirect('admin:index')  # Redirect admin to the admin dashboard
        logger.info(f'User {request.user.username} is already authenticated.')
        return redirect('index')  # Redirect to the index page

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next')  # Get the next URL from the form
        logger.debug(f'Attempting to authenticate user: {username}')  # Log the username attempt
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If credentials are correct, log the user in
            login(request, user)
            user_name = user.username
            logger.info(f'User {username} logged in successfully.')  # Log successful login
            # Always redirect to index after login
            return redirect(next_url or 'index')
        else:
            messages.error(request, 'Invalid username or password.')
            logger.warning(f'Failed login attempt for user: {username}')
            return render(request, 'index.html', {'user_name': user_name})

    # Render the index page with the login form if not authenticated
    return render(request, 'index.html', {'user_name': user_name})



def clear_login_modal_flag(request):
    """ Clear the session flag to prevent the modal from showing again. """
    if request.method == 'POST':  # We expect a POST request to clear the session flag
        if 'show_login_modal' in request.session:
            del request.session['show_login_modal']
        return JsonResponse({'message': 'Login modal flag cleared'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)



def manage_sections(request, model_name):
    if model_name == 'company':
        form = CompanyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('manage_sections', model_name='company')
        companies = Company.objects.all()
        company_table = CompanyTable(companies)

        return render(request, 'manage_sections.html', {
            'model_name': 'company',
            'company_form': form,
            'company_table': company_table,
        })

    elif model_name == 'department':
        form = DepartmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('manage_sections', model_name='department')
        departments = Department.objects.all()
        department_table = DepartmentTable(departments)

        return render(request, 'manage_sections.html', {
            'model_name': 'department',
            'department_form': form,
            'department_table': department_table,
        })

    elif model_name == 'affiliate':
        form = AffiliateForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('manage_sections', model_name='affiliate')
        affiliates = Affiliate.objects.all()
        affiliate_table = AffiliateTable(affiliates)

        return render(request, 'manage_sections.html', {
            'model_name': 'affiliate',
            'affiliate_form': form,
            'affiliate_table': affiliate_table,
        })

    elif model_name == 'employee':
        form = EmployeeForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('manage_sections', model_name='employee')
        employees = Employee.objects.all()
        employee_table = EmployeeTable(employees)

        return render(request, 'manage_sections.html', {
            'model_name': 'employee',
            'employee_form': form,
            'employee_table': employee_table,
        })

    else:
        return render(request, 'manage_sections.html', {
            'model_name': None,
        })