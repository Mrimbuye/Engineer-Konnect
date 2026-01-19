from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def register(request):
    return render(request, 'register.html')

@require_http_methods(["GET"])
def login(request):
    return render(request, 'login.html')

@require_http_methods(["GET"])
def dashboard(request):
    return render(request, 'dashboard.html')

@require_http_methods(["GET"])
def profile(request):
    return render(request, 'profile.html')

@require_http_methods(["GET"])
def profile_edit(request):
    return render(request, 'profile_edit.html')

@require_http_methods(["GET"])
def discussions(request):
    return render(request, 'discussions.html')

@require_http_methods(["GET"])
def jobs(request):
    return render(request, 'jobs.html')

@require_http_methods(["GET"])
def messages(request):
    return render(request, 'messages.html')
@require_http_methods(["GET"])
def connections(request):
    return render(request, 'connections.html')

@require_http_methods(["GET"])
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    return render(request, 'admin_dashboard.html')
