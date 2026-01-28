from applications.models import Application
from rest_framework.serializers import ModelSerializer, ReadOnlyField, CharField
from authentication.models import User, UserRole
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import ValidationError

class ApplicationSerializer(ModelSerializer):
    student = ReadOnlyField(source='student.email')

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['status']

class UserRegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        
    def create(self, validated_data):
        password = validated_data.get('password')
        
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationError({"password": list(e.messages)})
        
        return User.objects.create_user(**validated_data)

class UserRoleSerializer(ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'title', 'is_active']


