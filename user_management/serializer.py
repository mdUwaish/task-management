from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'phone_number', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role', 'phone_number', 'can_create_tasks', 'can_assign_tasks', 'can_view_all_tasks']
    
    extra_kwargs = {
        'password': {'write_only': True},
        'can_create_tasks': {'read_only': True},
        'can_assign_tasks': {'read_only': True},
        'can_view_all_tasks': {'read_only': True},
    }

    def update(self, instance, validated_data):
        request = self.context.get('request')
        
        if request and request.user.role not in ['Admin', 'Manager']:
            validated_data.pop('role', None)
            validated_data.pop('can_create_tasks', None)
            validated_data.pop('can_assign_tasks', None)
            validated_data.pop('can_view_all_tasks', None)

        if 'password' in validated_data:
            validated_data.pop('password')

        return super().update(instance, validated_data)