from rest_framework import serializers
from .models import Task
from user_management.models import User

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'completed_at', 'task_type', 'status', 'assigned_users']

    def get_assigned_users(self, obj):
        return [user.email for user in obj.assigned_users.all()]


class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_users = serializers.ListField(child=serializers.EmailField())

    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type', 'status', 'assigned_users']

    def validate_assigned_users(self, value):
        users = User.objects.filter(email__in=value)
        if len(users) != len(value):
            raise serializers.ValidationError("Some users not found.")
        return users

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_users')
        task = Task.objects.create(**validated_data)
        task.assigned_users.set(assigned_users)
        return task


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']

    def validate(self, data):
        request_user = self.context['request'].user
        task = self.instance
        
        if request_user not in task.assigned_users.all():
            raise serializers.ValidationError("You are not assigned to this task.")
        
        return data