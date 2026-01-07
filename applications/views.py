from django.shortcuts import render, redirect, get_object_or_404
from .models import Application
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# Create your views here.

@login_required
def submit_application(request):
    if request.method == 'POST':
        university_name = request.POST.get('university_name')
        program_name = request.POST.get('program_name')
        study_mode = request.POST.get('study_mode')
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        Application.objects.create(
            university_name = university_name,
            program_name = program_name,
            study_mode = study_mode,
            subject = subject,
            content = content,
            student = request.user
        )

        messages.success(request, "Alication submmited successfully")
        return redirect('stddashbord')
    
    return render(request, 'application/addapplication.html')


@login_required
@require_POST
def accept_application(request):
    app_id = request.POST.get('application_id')
    application = get_object_or_404(Application, application_id=app_id)
    application.status = 'Accepted'
    application.save()
    return JsonResponse({
        'status': 'Accepted',
        'accepted': Application.objects.filter(status='Accepted').count(),
        'rejected': Application.objects.filter(status='Rejected').count(),
        'pending': Application.objects.filter(status='Pending').count(),
    })

@login_required
@require_POST
def reject_application(request):
    app_id = request.POST.get('application_id')
    application = get_object_or_404(Application, application_id=app_id)

    application.status = 'Rejected'
    application.save()

    return JsonResponse({
        'status': 'Rejected',
        'accepted': Application.objects.filter(status='Accepted').count(),
        'rejected': Application.objects.filter(status='Rejected').count(),
        'pending': Application.objects.filter(status='Pending').count(),
    })