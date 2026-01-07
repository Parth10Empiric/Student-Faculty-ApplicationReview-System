from django.contrib import admin
from .models import User, UserRole

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    
    list_filter = ('role', 'is_staff')
    
    search_fields = ('email', 'first_name', 'last_name')
    
    ordering = ('email',)

# Register your models
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserRole)
# admin.site.register(Application)