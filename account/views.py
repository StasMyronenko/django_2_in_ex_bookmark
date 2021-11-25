from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail

from .models import Profile

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages  # Уведомления


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.data
            print(cd)
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])

            # Сохраняем пользователя в базе данных.

            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required  # выполняет функцию только если пользователь авторизирован
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        try:
            profile_form = ProfileEditForm(instance=request.user.profile)
        except:
            new_user = user_form.save(commit=False)
            new_user.save()
            Profile.objects.create(user=new_user)
            profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})