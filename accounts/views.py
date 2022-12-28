import datetime as dt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ContactForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from scraping.models import Error
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Вы вошли в систему с email: {user}')
        return redirect('scraping:home')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Вы вышли из системы')
    return redirect('accounts:login')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.add_message(request, messages.SUCCESS, f'Пользователь {new_user} успешно создан 😀')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})

    return render(request, 'accounts/register.html', {'form': form})


@login_required()
def update_view(request):
    contact_form = ContactForm()
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(instance=request.user, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.city = data['city']
            user.language = data['language']
            user.send_email = data['send_email']
            user.email = data['email']
            user.save()
            messages.add_message(request, messages.INFO, f'Настройки аккаунта {user}, изменены.')
            return redirect('accounts:update')
    else:
        form = UserUpdateForm(instance=request.user,
                              initial={'city': user.city, 'language': user.language,
                                       'send_email': user.send_email, 'email': user.email})
    return render(request, 'accounts/update.html', {'form': form, 'contact_form': contact_form})


@login_required()
def delete_view(request):
    user = request.user
    if request.method == 'POST':
        qs = User.objects.get(pk=user.pk)
        qs.delete()
        messages.add_message(request, messages.ERROR, f'Пользователь {user} удален :(')
    return redirect('accounts:login')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'language': language, 'email': email, })
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [{'city': city, 'language': language, 'email': email, }]}
                Error(data=data).save()

            messages.add_message(request, messages.INFO, 'Данные отправлены администрации сайта 🙄')
            return redirect('accounts:update')
        else:
            redirect('accounts:update')
    else:
        redirect('accounts:login')


class PasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:update')
    success_message = 'Смена пароля прошла успешно :)'


class PasswordReset(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    subject_template_name = 'accounts/reset_subject.txt'
    email_template_name = 'accounts/email_subject.txt'
    success_url = reverse_lazy('accounts:login')
    success_message = 'Письмо успешно отправлено по указанному email :)'


class PasswordConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_confirm.html'
    post_reset_login = True
    success_message = 'Ваш пароль успешно востановлен :)'
    success_url = reverse_lazy('accounts:update')

