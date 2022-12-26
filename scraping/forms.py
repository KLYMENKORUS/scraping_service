from django import forms
from .models import City, Language


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Город',
        empty_label='Выбирете город'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность',
        empty_label='Выбирете специальность'
    )
