
from django import forms
from django.contrib.auth.models import User


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.core.exceptions import ObjectDoesNotExist


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Podaj hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))


    def clean_password2(self):
        user = self.cleaned_data
        if user['password2'] != user['password']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return user['password2']

    def clean_email(self):
        user = self.cleaned_data
        if User.objects.filter(username=user['email']).exists():
            raise forms.ValidationError('Użytkownik o takim emailu już istnieje!')
        return user['email']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

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

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            return username
        except ObjectDoesNotExist:
            raise forms.ValidationError('Niepoprawna nazwa użytkownika')

    def clean_password(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = User.objects.get(username=username)
            if user.check_password(password):
                return password
            raise forms.ValidationError('Niepoprawne hasło')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_superuser', 'is_active']
        labels = {
            'username': 'nazwaużytkownika',
            'first_name': 'imię',
            'last_name': 'nazwisko',
            'is_superuser': 'super użytkownik',
            'is_active': 'konto aktywne',
        }


class SettingsUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Podaj hasło'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'imię',
            'last_name': 'nazwisko',
            'email': 'adres e-mail',
        }

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Podaj aktualne hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Podaj nowe hasło'}))
    password3 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Podaj nowe hasło (powtórz)'}))


    def clean(self):
        cleaned_data = super().clean()
        password2 = cleaned_data['password2']
        password3 = cleaned_data['password3']
        if password2 != password3:
            raise forms.ValidationError('Podałeś inne hasła')

    def clean_password(self):
            password = self.cleaned_data['password']
            user = User.objects.get(username=username)# jak pobrać aktualnego usera
            if user.check_password(password):
                return password
            raise forms.ValidationError('Niepoprawne hasło')