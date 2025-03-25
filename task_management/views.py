from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from user_management.models import User
from .serializer import TaskSerializer, TaskCreateSerializer
from .permissions import CanManageTasks, IsTaskAssignee


class CreateTask(APIView):
    permission_classes = [IsAuthenticated, CanManageTasks]

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignTask(APIView):
    permission_classes = [IsAuthenticated, CanManageTasks]

    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        user_emails = request.data.get("assigned_users", [])
        users = User.objects.filter(email__in=user_emails)
        if not users:
            return Response({"error": "Users not found"}, status=status.HTTP_400_BAD_REQUEST)

        task.assigned_users.add(*users)
        return Response({"message": "Task assigned successfully"}, status=status.HTTP_200_OK)


class UserTasks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_users=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskStatusUpdate(APIView):
    permission_classes = [IsAuthenticated, IsTaskAssignee]

    def patch(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_status = request.data.get("status")

        if not new_status:
            return Response({"error": "Status field is required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in ["Pending", "In Progress", "Completed"]:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        task.status = new_status
        task.save()

        return Response({"message": "Task status updated successfully", "task": TaskSerializer(task).data}, status=status.HTTP_200_OK)