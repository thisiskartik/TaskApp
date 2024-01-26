from datetime import date
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from .serializers import TaskSerializer
from .utils import get_task_priority
from .models import Task


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.request.user.task_set.filter(is_deleted=False)
        if self.request.method == 'GET':
            if 'priority' in self.request.GET:
                queryset = queryset.filter(priority=int(self.request.GET['priority']))
            if 'due_date' in self.request.GET:
                queryset = queryset.filter(due_date=date.fromisoformat(self.request.GET['due_date']))
        return queryset

    def perform_create(self, serializer):
        errors = {}
        if 'title' not in self.request.data:
            errors['title'] = ['This field is required']
        if 'description' not in self.request.data:
            errors['description'] = ['This field is required']
        if 'due_date' not in self.request.data:
            errors['due_date'] = ['This field is required']
        if errors:
            raise ValidationError(errors)

        if serializer.validated_data.get('due_date') < date.today():
            raise ValidationError({'due_date': 'Due date cannot be in the past.'})

        serializer.save(user=self.request.user,
                        priority=get_task_priority(serializer.validated_data.get('due_date')))

    def perform_update(self, serializer):
        if any(x in self.request.data for x in ['title', 'description', 'priority', 'user', 'is_deleted']):
            raise ValidationError("Only due_date and status can be updated")

        if 'status' in serializer.validated_data:
            if serializer.validated_data.get('status') not in ['TODO', 'DONE']:
                raise ValidationError({"status": ["Status can only be updated to TODO or DONE"]})
            for subtask in Task.objects.get(id=self.kwargs['pk']).subtask_set.all():
                if serializer.validated_data.get('status') == 'TODO':
                    subtask.status = 0
                elif serializer.validated_data.get('status') == 'DONE':
                    subtask.status = 1
                subtask.save()

        if 'due_date' in serializer.validated_data:
            if serializer.validated_data.get('due_date') < date.today():
                raise ValidationError({'due_date': 'Due date cannot be in the past.'})
            print(get_task_priority(serializer.validated_data.get('due_date')))
            serializer.save(priority=get_task_priority(serializer.validated_data.get('due_date')))
        else:
            serializer.save()

    def perform_destroy(self, instance):
        for subtask in instance.subtask_set.filter(is_deleted=False):
            subtask.is_deleted = True
            subtask.save()
        instance.is_deleted = True
        instance.save()
