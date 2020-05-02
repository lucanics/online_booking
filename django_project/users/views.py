from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            vorname = form.cleaned_data.get('vorname')
            nachname = form.cleaned_data.get('nachname')
            adresse = form.cleaned_data.get('adresse')
            tel = form.cleaned_data.get('tel')

            user = User.objects.get(username=username)
            user.profile.vorname = vorname
            user.profile.nachname = nachname
            user.profile.adresse = adresse
            user.profile.tel = tel
            user.profile.email = username
            user.save()
            messages.success(request, f'Your account has been created {vorname}! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)
