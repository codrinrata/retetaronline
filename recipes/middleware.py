from django.shortcuts import redirect
from django.urls import reverse

class SimpleAuthMiddleware:
    """
    Middleware to protect all pages except login pages
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that don't require authentication
        self.public_paths = [
            '/simple-login/',
            '/admin-login/',
            '/admin/',
        ]

    def __call__(self, request):
        # Check if user is authenticated via session or Django admin
        is_authenticated = (
            request.session.get('is_authenticated') or 
            request.user.is_authenticated
        )
        
        # Check if current path is public
        is_public_path = any(
            request.path.startswith(path) 
            for path in self.public_paths
        )
        
        # Redirect to login if not authenticated and not on public path
        if not is_authenticated and not is_public_path:
            return redirect('recipes:simple_login')
        
        response = self.get_response(request)
        return response
