from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.RecipeListView.as_view(), name='list'),
    path('create/', views.RecipeCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.RecipeDetailView.as_view(), name='detail'),
]
