from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomAuthenticationForm(AuthenticationForm):
    #email = forms.EmailField(required=True)
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField(required=True)
    vorname = forms.CharField(required=True, )
    nachname = forms.CharField(required=True)
    adresse = forms.CharField(required=False)
    tel = forms.CharField(required=False)

    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        #fields = ['email', 'vorname', 'nachname']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # parent's classe's save function


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField(required=True)
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    class Meta:
        model = User
        fields = ['username'] # allows us to update username

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image'] # allows us to update the profile image