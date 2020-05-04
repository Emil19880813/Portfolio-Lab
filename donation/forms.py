
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Podaj hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))


    def clean_password2(self):
        user = self.cleaned_data
        if user['password2'] != user['password']:
            raise ValidationError('Hasła nie są identyczne.')
        return user['password2']

    def clean_email(self):
        user = self.cleaned_data
        if User.objects.filter(username=user['email']).exists():
            raise ValidationError('Użytkownik o takim emailu już istnieje!')
        return user['email']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('first_name', placeholder='Imię'),
            Field('last_name', placeholder="Nazwisko"),
            Field('email', placeholder='Email'),
            Field('password', placeholder='Podaj hasło'),
            Field('password2', placeholder='Powtórz hasło')
        )