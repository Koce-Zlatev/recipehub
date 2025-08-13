from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Profile
from .forms import ProfileForm             # ← НОВО
from recipes.models import Favorite, Collection


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Успешна регистрация! Влез с новия си акаунт.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    fav_count = Favorite.objects.filter(user=request.user).count()
    collections_count = Collection.objects.filter(owner=request.user).count()
    context = {
        'profile': profile,
        'fav_count': fav_count,
        'collections_count': collections_count,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def favorites_list(request):
    favs = Favorite.objects.filter(user=request.user).select_related('recipe').order_by('-created_at')
    return render(request, 'accounts/favorites.html', {'favorites': favs})


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профилът е обновен.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})
