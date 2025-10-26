from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.cache import cache
from .models import Recipe

# Create your views here.

def simple_login(request):
    """Simple password-only login with rate limiting"""
    ip_address = request.META.get('REMOTE_ADDR')
    cache_key = f'login_attempts_{ip_address}'
    
    # Check if IP is blocked (too many failed attempts)
    attempts = cache.get(cache_key, 0)
    if attempts >= 5:
        return render(request, 'recipes/simple_login.html', {
            'blocked': True,
            'wait_time': 15
        })
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        if password == settings.SIMPLE_ACCESS_PASSWORD:
            request.session['is_authenticated'] = True
            # Clear failed attempts on successful login
            cache.delete(cache_key)
            messages.success(request, 'Welcome! You are now logged in.')
            return redirect('recipes:recipe_list')
        else:
            # Increment failed attempts
            cache.set(cache_key, attempts + 1, 900)  # Block for 15 minutes
            remaining = 5 - (attempts + 1)
            if remaining > 0:
                messages.error(request, f'Incorrect password. {remaining} attempts remaining.')
            else:
                messages.error(request, 'Too many failed attempts. Please wait 15 minutes.')
    
    return render(request, 'recipes/simple_login.html')

def admin_login(request):
    """Full admin login with username and password"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('recipes:recipe_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'recipes/admin_login.html')

def logout_view(request):
    """Logout user"""
    logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('recipes:simple_login')

def recipe_list(request):
    """Display all recipes"""
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    """Display a single recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def recipe_create(request):
    """Create a new recipe"""
    if request.method == 'POST':
        title = request.POST.get('title').capitalize()
        category = request.POST.get('category').capitalize()
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        
        # Simple validation
        if title and category and ingredients and instructions:
            Recipe.objects.create(
                title=title,
                category=category,
                ingredients=ingredients,
                instructions=instructions
            )
            messages.success(request, f'Recipe "{title}" created successfully!')
            return redirect('recipes:recipe_list')
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'recipes/recipe_form.html')

def recipe_update(request, pk):
    """Update an existing recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        recipe.title = request.POST.get('title')
        recipe.category = request.POST.get('category')
        recipe.ingredients = request.POST.get('ingredients')
        recipe.instructions = request.POST.get('instructions')
        
        if recipe.title and recipe.category and recipe.ingredients and recipe.instructions:
            recipe.save()
            messages.success(request, f'Recipe "{recipe.title}" updated successfully!')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'recipes/recipe_form.html', {'recipe': recipe})

def recipe_delete(request, pk):
    """Delete a recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        title = recipe.title
        recipe.delete()
        messages.success(request, f'Recipe "{title}" deleted successfully!')
        return redirect('recipes:recipe_list')
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

def category_list(request):
    """Display all categories with recipe counts"""
    from django.db.models import Count
    
    # Get categories with their recipe counts
    categories = (Recipe.objects
                  .values('category')
                  .annotate(count=Count('id'))
                  .order_by('category'))
    
    return render(request, 'recipes/category_list.html', {'categories': categories})

def category_recipes(request, category):
    """Display recipes filtered by category"""
    recipes = Recipe.objects.filter(category=category).order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'category': category,
        'is_filtered': True
    })
