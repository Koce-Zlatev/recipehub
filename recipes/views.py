from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Recipe
from .forms import RecipeForm

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    paginate_by = 10

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    slug_field = 'slug'

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