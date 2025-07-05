from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Task,attendees
from .forms import TaskForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
import json


def start_page(request):
    return render(request,'start_page.html')

def login_page(request):
    return render(request,'login.html')


def task_list(request):
    tasks = Task.objects.all()    # Retrieve all tasks

    if request.method == 'POST':    # Handle form submissions
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to avoid duplicate submissions
    else:
        form = TaskForm()

    # Pass tasks and the form to the template
    return render(request, 'task_list.html', {'tasks': tasks, 'form': form})

def mark_task_done(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = True
        task.save()
        messages.success(request, f'Task "{task.title}" marked as done!')
    return redirect('task_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.save()
        messages.success(request, f'Task updated successfully!')
    
    return redirect('task_list')

def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted!')
    return redirect('task_list')

def login_page(request):
    """Render the login page"""
    return render(request, 'auth/login.html')

@require_http_methods(["POST"])
def signup_view(request):
    """Handle user registration"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['full_name', 'user_name', 'email', 'pass_code']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Validate field lengths according to your model
        if len(data['email']) > 20:
            return JsonResponse({'error': 'Email must be 20 characters or less'}, status=400)
        
        if len(data['user_name']) > 200:
            return JsonResponse({'error': 'Username must be 200 characters or less'}, status=400)
        
        if len(data['full_name']) > 50:
            return JsonResponse({'error': 'Full name must be 50 characters or less'}, status=400)
        
        # Check if email already exists
        if attendees.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'An account with this email already exists'}, status=400)
        
        # Check if username already exists
        if attendees.objects.filter(user_name=data['user_name']).exists():
            return JsonResponse({'error': 'This username is already taken'}, status=400)
        
        # Hash the password
        hashed_password = make_password(data['pass_code'])
        
        # Create new attendee
        attendee = attendees.objects.create(
            full_name=data['full_name'],
            user_name=data['user_name'],
            email=data['email'],
            pass_code=hashed_password
        )
        
        return JsonResponse({
            'message': 'Account created successfully',
            'user_id': attendee.id
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except IntegrityError:
        return JsonResponse({'error': 'Account creation failed. Please try again.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

@require_http_methods(["POST"])
def signin_view(request):
    """Handle user sign in"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        # Find user by email
        try:
            attendee = attendees.objects.get(email=data['email'])
        except attendees.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
        
        # Check password
        if check_password(data['password'], attendee.pass_code):
            # Store user session (you can customize this)
            request.session['user_id'] = attendee.id
            request.session['user_name'] = attendee.user_name
            request.session['full_name'] = attendee.full_name
            
            return JsonResponse({
                'message': 'Sign in successful',
                'user': {
                    'id': attendee.id,
                    'user_name': attendee.user_name,
                    'full_name': attendee.full_name,
                    'email': attendee.email
                }
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

def logout_view(request):
    """Handle user logout"""
    request.session.flush()
    return redirect('login_page')

def dashboard_view(request):
    """Dashboard view for authenticated users"""
    if 'user_id' not in request.session:
        return redirect('login_page')
    
    user_data = {
        'user_id': request.session.get('user_id'),
        'user_name': request.session.get('user_name'),
        'full_name': request.session.get('full_name')
    }
    
    return render(request, 'dashboard.html', {'user': user_data})