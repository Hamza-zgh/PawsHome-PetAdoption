from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm  # We'll create this form next
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.MEMBER
            user.save()
            return redirect(reverse('login'))
        else:
            # Print detailed form errors
            print("Form errors:")
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('home'))  # Redirect to admin or dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm(request)

    return render(request, 'users/login.html', {'form': form})
def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect(reverse('login'))