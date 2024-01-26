import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import SubTaskSerializer
from .models import SubTask


class SubTaskViewSet(ModelViewSet):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == 'GET' and 'task_id' in self.request.GET:
            return self.request.user.task_set.get(id=self.request.GET['task_id']).subtask_set.filter(is_deleted=False)
        else:
            subtasks = SubTask.objects.none()
            for task in self.request.user.task_set.filter(is_deleted=False):
                subtasks |= task.subtask_set.filter(is_deleted=False)
            return subtasks

    def perform_create(self, serializer):
        if 'task' not in self.request.data:
            raise ValidationError({"task": ["Task cannot be empty"]})
        if self.request.user != serializer.validated_data.get('task').user:
            raise ValidationError({"task": ["Cannot add sub task to other user\'s task"]})
        serializer.save(status=0)

    def perform_update(self, serializer):
        if any(x in self.request.data for x in ['task', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']):
            raise ValidationError("Only status can be updated")
        if 'status' not in self.request.data:
            raise ValidationError({"status": ["Status cannot be empty"]})
        serializer.save()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = datetime.datetime.now()
        instance.save()
