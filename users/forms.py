from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make first_name and last_name required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        # Remove username autofocus
        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['first_name'].widget.attrs['autofocus'] = True

        # Add Bootstrap classes and handle errors
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



        # Special handling for password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control pe-5 password-input',
            'onpaste': 'return false'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control pe-5 password-input',
            'onpaste': 'return false'
        })


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Properly set the password from password1
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'profession', 'state', 'city', 'address',
            'birth_date', 'gender', 'phone_number',
            'password1', 'password2'  # From UserCreationForm
        ]
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )