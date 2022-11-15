from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from airflow.models import *

# Create your views here.


def register_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'You\'re already logged in!')
        return redirect('/flights')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use')
                return redirect('/register')
            else:
                admin_key = request.POST['admin_key']
                if admin_key != '':
                    if len(AdminKey.objects.filter(a_key=admin_key)) > 0:
                        user_new = User.objects.create_user(username=username, password=password1, email=email,
                                                            first_name=first_name, last_name=last_name, is_staff=True)
                        user_new.save()
                        messages.info(request, 'Successfully registered')
                        return redirect('/login')
                    else:
                        messages.info(request, 'Wrong admin key')
                        return redirect('/register')
                else:
                    user_new = User.objects.create_user(username=username, password=password1, email=email,
                                                        first_name=first_name, last_name=last_name)
                    user_new.save()
                    messages.info(request, 'Successfully registered')
                    return redirect('/login')
        else:
            messages.info(request, 'Passwords don\'t match')
            return redirect('/register')

    else:
        return render(request, 'users/register.html')


def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'You\'re already logged in!')
        return redirect('/flights')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/flights')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('/login')
    else:
        return render(request, 'users/login.html')


def logout_page(request):
    auth.logout(request)
    messages.info(request, 'Successfully logged out')
    return redirect('/login')
