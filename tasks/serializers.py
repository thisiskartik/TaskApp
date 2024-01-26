from rest_framework.serializers import ModelSerializer
from .models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'priority', 'status')
        extra_kwargs = {"priority": {"required": False, "allow_null": True},
                        "title": {"required": False, "allow_null": True},
                        "description": {"required": False, "allow_null": True},
                        "due_date": {"required": False, "allow_null": True}}
