from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User, UserRole
from django.views.decorators.csrf import ensure_csrf_cookie 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from applications.models import Application
from .forms import ProfileUpdateForm
from django.views.decorators.cache import never_cache, cache_control
import re

def home_view(request):
    # if request.user.is_authenticated:
    #     if hasattr(request.user, 'role') and request.user.role is not None:
    #         return redirect('facdashbord' if request.user.role.title == 'Faculty' else 'stddashbord')
    #     return redirect('/admin/')
    return render(request, 'home/home.html')


def is_valid_password(password):

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*()_+=\-{}[\]:;"\'<,>.?/\\|]', password):
        return False, "Password must contain at least one special character."
    return True, ""


def register_view(request):
    if request.method == 'POST':
        
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role_title = request.POST.get('role')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'auth/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'auth/register.html')
        is_velid, message = is_valid_password(password)

        if not is_velid:
            messages.error(request, message)
            return render(request, 'auth/register.html')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'auth/register.html')

        try:
            role_obj = UserRole.objects.get(title=role_title)
            user = User.objects.create_user(
                email=email, password=password, first_name=f_name, 
                last_name=l_name, role=role_obj
            )
            login(request, user)
            return redirect('stddashbord' if role_title == 'Student' else 'facdashbord')
        except Exception as e:
            messages.error(request, f"Registration failed please try again {e}")
            
    return render(request, 'auth/register.html')

def custom_403_handler(request, exception=None):
    messages.error(request, "Your session expired or was invalid. Please try again.")
    return redirect('home')

@ensure_csrf_cookie
@never_cache
def login_view(request):

    if request.user.is_authenticated:
        if hasattr(request.user, 'role') and request.user.role is not None:
            return redirect('facdashbord' if request.user.role.title == 'Faculty' else 'stddashbord')
        return redirect('/admin/')
    
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            # next_url = request.GET.get('next')
            # if next_url:
            #     return redirect(next_url)
            if user.role is not None:
                return redirect('facdashbord' if user.role.title == 'Faculty' else 'stddashbord')
            else: 
                return redirect('/admin/')
        messages.error(request, "Invalid Email or Password")
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('home')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def stddashbord(request): 
    applications = Application.objects.filter(student=request.user)

    contex = {
        'applications':applications,
        'total_applications':applications.all().count(),
        'accepted_count':applications.filter(status='Accepted').count(),
        'rejected_count':applications.filter(status='Rejected').count(),
        'pending_count':applications.filter(status='Pending').count(),
    }

    return render(request, 'dashbord/stddashbord.html', contex)


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Update Successfully")
            return redirect('stddashbord')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'auth/profile.html',{'form':form})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def facdashbord(request): 
    applications = Application.objects.all()

    contex = {
        'applications':applications,
        'total_applications':applications.all().count(),
        'accepted_count':applications.filter(status='Accepted').count(),
        'rejected_count':applications.filter(status='Rejected').count(),
        'pending_count':applications.filter(status='Pending').count(),
    }
    return render(request, 'dashbord/facdashbord.html',contex)