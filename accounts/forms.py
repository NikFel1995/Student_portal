from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }), label='Пароль')


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Логин')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Фамилия')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', }), label='Почта')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }), label='Повтор пароля')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')