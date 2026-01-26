from applications.models import Application
from rest_framework import serializers
from authentication.models import User, UserRole

class ApplicationSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.email')

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['status']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role']

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'title', 'is_active']


