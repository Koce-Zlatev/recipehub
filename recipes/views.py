from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Recipe, Favorite, Comment
from .forms import RecipeForm, CommentForm


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    paginate_by = 10


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        recipe = self.object
        # Favorites
        ctx['favorites_count'] = recipe.favorites.count()
        ctx['is_favorite'] = user.is_authenticated and recipe.favorites.filter(user=user).exists()
        # Comments
        ctx['comments'] = recipe.comments.select_related('author').order_by('-created_at')
        ctx['comment_form'] = CommentForm()
        return ctx


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_staff


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Рецептата е създадена!')
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/form.html'
    slug_field = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'Рецептата е обновена!')
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Recipe
    slug_field = 'slug'
    template_name = 'recipes/confirm_delete.html'
    success_url = reverse_lazy('recipes:list')

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'Рецептата е изтрита.')
        return super().delete(request, *args, **kwargs)


@login_required
def toggle_favorite(request, slug):
    if request.method != "POST":
        return redirect('recipes:detail', slug=slug)

    recipe = get_object_or_404(Recipe, slug=slug)
    existing = Favorite.objects.filter(user=request.user, recipe=recipe).first()
    if existing:
        existing.delete()
        messages.info(request, 'Премахнато от любими.')
    else:
        Favorite.objects.create(user=request.user, recipe=recipe)
        messages.success(request, 'Добавено в любими!')
    return redirect('recipes:detail', slug=slug)


# ===== Коментари =====

@require_POST
@login_required
def add_comment(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.recipe = recipe
        comment.author = request.user
        comment.save()
        messages.success(request, 'Коментарът е добавен.')
    else:
        messages.error(request, 'Моля, въведете валиден коментар.')
    return redirect('recipes:detail', slug=slug)


@require_POST
@login_required
def delete_comment(request, slug, pk):
    recipe = get_object_or_404(Recipe, slug=slug)
    comment = get_object_or_404(Comment, pk=pk, recipe=recipe)
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
        messages.info(request, 'Коментарът е изтрит.')
    else:
        messages.error(request, 'Нямате права да изтриете този коментар.')
    return redirect('recipes:detail', slug=slug)
