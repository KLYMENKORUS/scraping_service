from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages


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
        return render(request, 'accounts/register_done.html', {'new_user': new_user})

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def update_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.city = data['city']
            user.language = data['language']
            user.send_email = data['send_email']
            user.save()
            messages.add_message(request, messages.INFO, f'Настройки аккаунта {user}, изменены.')
            return redirect('accounts:update')
    else:
        form = UserUpdateForm(
            initial={'city': user.city, 'language': user.language,
                     'send_email': user.send_email})
        return render(request, 'accounts/update.html', {'form': form})


@login_required
def delete_view(request):
    user = request.user
    if request.method == 'POST':
        qs = User.objects.get(pk=user.pk)
        qs.delete()
        messages.add_message(request, messages.ERROR, f'Пользователь {user} удален :(')
    return redirect('accounts:login')
