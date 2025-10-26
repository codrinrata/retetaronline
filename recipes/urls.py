from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Authentication
    path('simple-login/', views.simple_login, name='simple_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Recipe pages
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/new/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/edit/', views.recipe_update, name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<str:category>/', views.category_recipes, name='category_recipes'),
]
