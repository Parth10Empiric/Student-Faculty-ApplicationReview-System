from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterAPI,
    LoginAPI,
    StudentApplicationViewSet,
    FacultyApplicationViewSet,
    UserRoleViewset
)

router = DefaultRouter()
router.register(r'student/applications', StudentApplicationViewSet, basename='student-applications')
router.register(r'faculty/applications', FacultyApplicationViewSet, basename='faculty-applications')
router.register(r'userrole', UserRoleViewset, basename='userrole')
urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
