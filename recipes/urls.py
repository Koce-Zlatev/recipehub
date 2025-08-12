from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='list'),
    path('create/', views.RecipeCreateView.as_view(), name='create'),
    path('<slug:slug>/edit/', views.RecipeUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.RecipeDeleteView.as_view(), name='delete'),
    path('<slug:slug>/favorite/', views.toggle_favorite, name='favorite'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('<slug:slug>/comment/<int:pk>/delete/', views.delete_comment, name='del_comment'),
    path('<slug:slug>/', views.RecipeDetailView.as_view(), name='detail'),
]
