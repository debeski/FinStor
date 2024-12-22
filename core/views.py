from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


logger = logging.getLogger('documents')


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

