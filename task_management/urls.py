from django.urls import path
from .views import CreateTask, AssignTask, UserTasks, TaskStatusUpdate

urlpatterns = [
    path('tasks/', CreateTask.as_view()),
    path('tasks/<int:task_id>/assign/', AssignTask.as_view()),
    path('tasks/me/', UserTasks.as_view()),
    path('tasks/<int:pk>/update-status/', TaskStatusUpdate.as_view()),
]
