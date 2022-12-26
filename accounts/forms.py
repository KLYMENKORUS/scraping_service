from django import forms
from scraping.models import City, Language
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Ваш email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Ваш пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не верный!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Введите email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль повторно',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)
    
    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']


class UserUpdateForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug', required=True,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Город',
        empty_label='Выбирете город'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name='slug', required=True,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность',
        empty_label='Выбирете специальность'
    )
    email = forms.EmailField(label='Смена email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                    label='Получать рассылку')

    class Meta:
        model = User
        fields = ('city', 'language',  'email', 'send_email',)


class ContactForm(forms.Form):
    city = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}), label='Город')
    language = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}), label='Специальность'
                               )
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Введите email')