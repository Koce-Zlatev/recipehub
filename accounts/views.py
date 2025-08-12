from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from recipes.models import Favorite


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешна регистрация! Влез с новия си акаунт.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def favorites_list(request):
    favs = Favorite.objects.filter(user=request.user).select_related('recipe').order_by('-created_at')
    return render(request, 'accounts/favorites.html', {'favorites': favs})
