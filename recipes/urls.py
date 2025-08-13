from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='list'),
    path('create/', views.RecipeCreateView.as_view(), name='create'),

    path('collections/', views.CollectionListView.as_view(), name='collections'),
    path('collections/create/', views.CollectionCreateView.as_view(), name='collection-create'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    path('collections/<int:pk>/add/', views.add_to_collection, name='collection-add'),
    path('collections/<int:pk>/remove/<int:item_id>/', views.remove_from_collection, name='collection-remove'),

    path('<slug:slug>/edit/', views.RecipeUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.RecipeDeleteView.as_view(), name='delete'),
    path('<slug:slug>/favorite/', views.toggle_favorite, name='favorite'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('<slug:slug>/comment/<int:pk>/delete/', views.delete_comment, name='del_comment'),
    path('<slug:slug>/', views.RecipeDetailView.as_view(), name='detail'),
]
