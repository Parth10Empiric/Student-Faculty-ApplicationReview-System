from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.authtoken.models import Token
from rest_framework.serializers import Serializer, ChoiceField
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter

from .serializer import UserRegisterSerializer, ApplicationSerializer, UserRoleSerializer
from applications.models import Application
from .permission import IsFaculty, IsStudent
from authentication.models import UserRole


from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "message": "User registered successfully",
                "token": token.key,
                "created": token.created
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "role": user.role.title
            })
        return Response({"error": "Invalid credentials"}, status=401)


class StudentApplicationViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsStudent]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['application_id']
    
    def get_queryset(self):
        return Application.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class StatusUpdateSerializer(Serializer):
    status = ChoiceField(
        choices=['Accepted', 'Rejected', 'Pending'],
        required=True
    )


class FacultyApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsFaculty]
    queryset = Application.objects.all()

    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Faculty cannot atch applications")

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {'status': ['exact']}
    
    @action(detail=True, methods=['get', 'patch'], serializer_class=StatusUpdateSerializer)
    def status(self, request, pk=None):
        application = self.get_object()

        if request.method == 'GET':
            return Response({
                "application_id": application.application_id,
                "current_status": application.status
            })
            
        if application.status == 'Accepted':
            return Response({
                "message": "alredy Accepted you can not change"
            })

        if application.status == 'Rejected':
            return Response({
                "message": "alredy Rejected you can not change"
            })
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        application.status = serializer.validated_data['status']
        application.save()

        return Response({
            "message": "Status updated successfully",
            "new_status": application.status
        })
        

class UserRoleViewset(ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminUser]