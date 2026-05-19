from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

def index(request):
    return render(request, 'index.html')

def projects(request):
    projects_list = [
        {'title': 'Project A', 'description': 'A short description.'},
        {'title': 'Project B', 'description': 'Another short description.'},
    ]
    return render(request, 'projects.html', {'projects': projects_list})

@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        # In a real site you'd save/send the message. Here we just show a success page.
        return render(request, 'contact.html', {'sent': True, 'name': name})
    return render(request, 'contact.html')
