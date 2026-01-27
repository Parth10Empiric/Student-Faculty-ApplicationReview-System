from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.serializers import Serializer, ChoiceField
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.authentication import TokenAuthentication
from .serializer import UserRegisterSerializer, ApplicationSerializer, UserRoleSerializer
from applications.models import Application
from .permission import IsFaculty, IsStudent
from authentication.models import UserRole

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


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
    
# class LoginAPI(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(email=email, password=password)
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({
#                 "token": token.key,
#                 "role": user.role.title
#             })
#         return Response({"error": "Invalid credentials"}, status=401)

class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            
            return Response({
                "message": "Login successful",
                "token": token.key,
                "role": user.role.title
            }, status=status.HTTP_200_OK)
            
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# class StudentDashboardAPI(APIView):
#     permission_classes = [IsStudent]

#     def get(self, request):
#         applications = Application.objects.filter(student=request.user)
#         serializer = ApplicationSerializer(applications, many=True)
#         return Response(serializer.data)

# --------------
# class StudentApplicationViewSet(ModelViewSet):
#     serializer_class = ApplicationSerializer
#     permission_classes = [IsStudent]

#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['status']
#     search_fields = ['application_id']
    
#     def get_queryset(self):
#         return Application.objects.filter(student=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(student=self.request.user)
# -----------------------

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



# class ApplicationCreateAPI(APIView):
#     permission_classes = [IsStudent]

#     def post(self, request):
#         serializer = ApplicationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(student=request.user)
#             return Response({"message": "Application submitted"}, status=201)
#         return Response(serializer.errors, status=400)

class StatusUpdateSerializer(Serializer):
    status = ChoiceField(
        choices=['Accepted', 'Rejected'],
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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        application.status = serializer.validated_data['status']
        application.save()

        return Response({
            "message": "Status updated successfully",
            "new_status": application.status
        })
        
        
# class FacultyDashboardAPI(ListModelMixin, GenericAPIView):
#     permission_classes = [IsFaculty]
#     queryset = Application.objects.all()
#     serializer_class = ApplicationSerializer

#     def get(self,request,*args, **kwargs):
#         return self.list(request, *args, **kwargs)

    # def get(self, request):
    #     applications = Application.objects.all()
    #     serializer = ApplicationSerializer(applications, many=True)
    #     return Response(serializer.data)

# class ApplicationStatusAPI(APIView):
#     permission_classes = [IsFaculty]

#     def patch(self, request, pk):
#         try:
#             application = Application.objects.get(pk=pk)
#         except Application.DoesNotExist:
#             return Response({"error": "Application not found"}, status=404)

#         status_value = request.data.get('status')
#         if status_value not in ['Accepted', 'Rejected']:
#             return Response({"error": "Invalid status"}, status=400)

#         application.status = status_value
#         application.save()
#         return Response({"message": f"Application {status_value}"})

class UserRoleViewset(ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminUser]