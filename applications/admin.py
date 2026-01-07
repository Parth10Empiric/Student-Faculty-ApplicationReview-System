from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'application_id',
        'university_name',
        'program_name',
        'student',
        'study_mode',
        'status',
        'subject',
    )

    list_filter = (
        'status',
        'study_mode',
        'university_name',
        'program_name',
    )

    search_fields = (
        'university_name',
        'program_name',
        'subject',
        'student__email',
        'student__first_name',
        'student__last_name',
    )

    list_editable = ('status',) 

    ordering = ('application_id',)

    fieldsets = (
        ('Application Details', {
            'fields': (
                'university_name',
                'program_name',
                'study_mode',
                'subject',
                'content',
            )
        }),
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
