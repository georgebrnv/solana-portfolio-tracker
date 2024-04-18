from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .decorators import redirect_authenticated_user

from .models import UserAuth

@redirect_authenticated_user
def register_user(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = UserAuth.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            return redirect('index')
        else:
            return redirect('register')

    else:
        return render(request, 'authentication/register.html')


@redirect_authenticated_user
def login_user(request):

    if request.method == 'POST':
        email_username = request.POST['email_username']
        password = request.POST['password']

        # Returns 'None' if credentials are invalid.
        user = authenticate(request, username=email_username, password=password)

        if user is None:
            user = authenticate(request, email=email_username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Authentication failed for both username and email
            return redirect('login')
    else:
        return render(request, 'authentication/login.html')


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'authentication/login.html')