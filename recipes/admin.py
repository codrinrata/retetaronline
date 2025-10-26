from django.contrib import admin
from .models import Recipe

# Register your models here.

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'ingredients', 'instructions']
    ordering = ['-created_at']
