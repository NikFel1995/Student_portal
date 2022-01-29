from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from .forms import LoginForm, UserRegistrationForm, PasswordChangeCustomForm
from django.contrib.auth import update_session_auth_hash


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('classroom:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if not request.user.is_authenticated:

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'Успешный вход на сайт!')
                        return redirect('accounts:profile')
                    else:
                        messages.error(request, 'Аккаунт деактивирован. Вход невозможен!')
                else:
                    messages.error(request, 'Неверный логин и/или пароль!')
        else:
            form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('accounts:profile')


def user_logout(request):
    logout(request)
    return redirect('accounts:login')


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html', {'user': request.user})
    else:
        return redirect('accounts:login')


def show_user_profile(request, profile_id):
    user = get_object_or_404(User, id=profile_id)
    if user is not None:
        return render(request, 'accounts/profile.html', {'user': user})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменен!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
